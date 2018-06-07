###Main module for OCR API application###
from __future__ import print_function
import os
import sys
import subprocess
import json
from PIL import Image
import logging

from flask import jsonify
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#configure pyhton logging module for log creation
logging.basicConfig(filename="/app/ocr.log",format='%(levelname)s:%(asctime)s:%(message)s', level=logging.DEBUG)

def notallowedfile():
    ocrreply = {
        "response":{
        "ocrtext":"Not allowed file type"
        },
    }
    with open('./ocr/casesdb.json', 'r') as f:
        cases = json.load(f)
    # return jsonify(ocr.file_not_found)
    return (cases["Not_Allowed_File_Ext"], ocrreply["response"])
#this function is used to run tesseract on the image file. Recieve the image file name
def ocr(image):
    print("ocr started", file=sys.stderr)
    logging.info(json.dumps({"action": "ocr started"}))
    command = ['tesseract', image, 'stdout']
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )

    out, err = p.communicate()
    print("ocr ended", file=sys.stderr)
    logging.info(json.dumps({"action": "ocr finished"}))
    return out, err
#
# #Spcial cases for OCR
# #case a file was not found
file_not_found = {
    "query" : "default"
}
# #case of ocr failure
# ocr_dir_not_work  = {
#     "query": "temp_profile_ocrfail"
# }
# #case of no text was found in the image
# no_text_found = {
#     "query": "ocr_notextfound"
# }

#Function to resize the image file by x3. This increase OCR accuracy
def resizeimage(filename):
    if os.path.getsize(filename) < 999999:
        img = Image.open(filename)
        size = (((img.size[0] * 3), (img.size[1] * 3)))
        img_resized = img.resize(size, Image.ANTIALIAS)
        img_resized.save(filename, "PNG")
        print("image resized", file=sys.stderr)
        logging.info(json.dumps({"action": "image resized"}))

#Function to send the file for OCR function and ruturn the results
def process_file(filename):
    print("start process file", file=sys.stderr)
    logging.info(json.dumps({"action": "file processing started"}))
    #validate that the file exist
    if not os.path.exists(filename):
        print("file not found true", file=sys.stderr)
        logging.warn(json.dumps({"error": "file not found"}))
        return 1, file_not_found

    #send the file for resize if needed
    resizeimage(filename)
    print("start ocr", file=sys.stderr)
    logging.info(json.dumps({"action": "file sent for ocr"}))

#Run OCR on the file using tesseract
    out, err = ocr(filename)
    print("finish ocr", file=sys.stderr)
    logging.info(json.dumps({"action": "returned from ocr"}))
    print(err, file=sys.stderr)
    print(out, file=sys.stderr)

#OCR API Output cases - search for the text from the OCR in the errors DB. Return the OCR text and query
    #prepare the OCR text to be returned by OCR API
    ocrreply = out.decode('utf-8')
    ocrdata = {
        "response":{
        "ocrtext":ocrreply
        },
    }
    #open the cases DB for search
    with open('./ocr/casesdb.json', 'r') as f:
        data = json.load(f)

    #Case of image file withou text in it
    if out == b' \n\x0c':
         return 2, (data["No_Text_Found"], ocrdata["response"])

    #Compare the OCR text with error from the cases DB
    best_fuz =0
    for key in data.keys():
        # Perform fuzzynes comparision between OCR text and casesDB
        fuzzyness = fuzz.partial_ratio(str(key).lower(), str(out).lower())
        logging.info(json.dumps([str(key).lower(), fuzzyness]))
        if fuzzyness > 50:
            if fuzzyness > best_fuz:
                best_key = key
                best_fuz = fuzzyness
            logging.info(json.dumps({"ocr status": "known issue", "ocr text": ocrreply}))
            #return 0, (data[key], ocrdata["response"])
            logging.info(json.dumps([str(key).lower(),fuzzyness]))
        # if str(key).lower() in str(out).lower():
        #      logging.info(json.dumps({"ocr status": "known issue", "ocr text":ocrreply}))
        #      return 0,(data[key],ocrdata["response"])
    if best_fuz > 0:
        return 0, (data[best_key], ocrdata["response"])

    #case that the OCR data was not found in the errors DB
    logging.info(json.dumps({"ocr status": "issue not recognized", "ocr text": ocrreply}))
    return 1, (data["topic_not_recognized"], ocrdata["response"])
