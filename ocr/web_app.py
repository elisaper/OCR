from __future__ import print_function
import os
import ocr
import sys
import logging
import json
import datetime


#configure pyhton logging module for log creation
logging.basicConfig(filename="/app/ocr.log",format='%(levelname)s:%(asctime)s:%(message)s', level=logging.DEBUG)

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join(root, "uploads")

@app.route("/")
def version():
    return "version 0.3.8"

@app.route("/api1/ocr/<path:filename>", methods=["GET"])
def runapp(filename):
    path = os.path.join("/", "opt", "screenshots", filename)
    exitcode, result = ocr.process_file(path)
    return jsonify(result)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#main route for post requests - validate the file type, save it, send to OCR function and ruturn the results
@app.route('/api1/ocr', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(ocr.file_not_found)
    file = request.files['file']
    if file.filename == '':
        return jsonify(ocr.file_not_found)

    if file and not allowed_file(file.filename):
        return jsonify(ocr.notallowedfile())
        # with open('./ocr/casesdb.json', 'r') as f:
        #     cases = json.load(f)
        # return (cases["Not_Allowed_File_Ext"])

    if file and allowed_file(file.filename):
        #add date and time to the file name
        format = "%Y-%m-%dT%H:%M:%S"
        now = datetime.datetime.utcnow().strftime(format)
        filename = now + '_' + file.filename
        filename = secure_filename(filename)
        print(filename, file=sys.stderr)
        logging.info(json.dumps({"filename": filename, "action": "file renamed"}))
        #Save the file to upload folder
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logging.info(json.dumps({"action":"start file save", "filename": filename}))
        print("start file save", file=sys.stderr)
        file.save(filepath)
        print("file saved", file=sys.stderr)
        logging.info(json.dumps({"action":"file saved"}))
        exitcode, result = ocr.process_file(filepath)
        logging.info(json.dumps({"action": "ocr process completed succesfully"}))
        return jsonify(result)
