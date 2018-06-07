import os
from ocr import ocr, process_file, cases, no_text_found, file_not_found, ocr_dir_not_work
import ocr.web_app as web
import requests
import json
class Testweb():


    def test_main_page(self):
        app = web.app.test_client()
        rv = app.get('/api1/ocr/Error1.jpg')
        assert json.loads(rv.data.decode('utf8')) == {"action": "input.unknown", "query": "Windows Cannot access"}

    def xtest_upload(self):
        app = web.app.test_client()
        #{'file': BytesIO(b"content")})
        #with open(os.path.join("screenshots", "Error1.jpg"), "rb") as fh:
        #    content = fh.read()#.encode('utf-8')
        content = b"hello"
        map_name_to_file_and_name = {"abc.jpg": (content, "mocked_name.jpg")}
        rv = app.post('/api1/ocr', data=map_name_to_file_and_name, content_type='multipart/form-data')
#        assert rv.status_code == 200
#        assert json.loads(rv.data.decode('utf8')) == {"action": "ShareAccessError"}

#        assert json.loads(rv.data.decode('utf8')) == {"action": "ShareAccessError"}

class TestOcr():

    def test_image(self):
        for name, expected in cases.items():
            image = os.path.join("screenshots", name)
            out, err = ocr(image)
            if "err" in expected:
                assert err == expected["err"]
            else:
                assert err == b""
            assert expected["ocr_out"] in out
        # ocrout = os.path.join("screenshots", name) + ".txt"
        # with open(ocrout, encoding='utf-8') as fh:
        #     expectedoutput = fh.read()
        # assert out == expectedoutput

        image = os.path.join("screenshots", "view.jpg")
        out, err = ocr(image)
        assert err == b"Warning. Invalid resolution 0 dpi. Using 70 instead.\n"
        assert  b' \n\n' == out


    def test_missing_image(self):
        out, err = ocr("image.png")
        assert b"Error during processing." in err
        assert out == b""

    def test_process_file(self):
        for name, expected in cases.items():
            image = os.path.join("screenshots", name)
            exitcode, result = process_file(image)
            assert exitcode == 0
            assert result == expected["response"]

        image = os.path.join("screenshots", "view.jpg")
        exitcode, result = process_file(image)
        assert exitcode == 3
        assert  result == no_text_found

        image = os.path.join("screenshots", "qqrq.jpg")
        exitcode, result = process_file(image)
        assert exitcode == 1
        assert  result == file_not_found

        image = os.path.join("screenshots", "error5.png")
        exitcode, result = process_file(image)
        assert exitcode == 2
        assert  result == ocr_dir_not_work

        image = os.path.join("screenshots", "Error8.jpeg")
        exitcode, result = process_file(image)
        assert exitcode == 0
        assert  result == cases["Error2.jpg"]["response"]

    def test_cfocr(self):
        url = "https://ocrdev.cfapps.eu10.hana.ondemand.com/api1/ocr"
        for name, expected in cases.items():
           if name not in ["Error1.jpg", "Error2.jpg", "Error3.jpg", "Error4.jpg", "error6.png", "Error7.jpg"]:
               continue
           image = os.path.join("screenshots", name)
           files = {'file': open(image, 'rb')}
           r = requests.post(url, files=files)
           assert r.json() == expected["response"]
