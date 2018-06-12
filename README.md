# Error_Recognition
Error recognition via OSR

running vagrant
    #vagrant up
    #vagrant ssh
    cd /vagrant

Docker
    Build Docker
        #docker build -t ocr .
    Running the environment
        #docker run -it -v $(pwd):/opt tesseractshadow/tesseract4re
        #docker run -it -p 0.0.0.0:8080:8080 -v $(pwd):/opt ocr
        #cd /opt/
        #python3 -m pytest
        #python3 test_ocr.py screenshots/Error2.jpg
    Delete images
        #sudo docker rm $(sudo docker ps -aq)
    Exit environment
        #Ctrl+D or exit to leave docker
        #exit (from vagrant)
        #vagrant halt
Running flask
        FLASK_APP=ocr/web_app.py flask run --host=0.0.0.0 --port=8080
        python3 -m flask run FLASK_APP=ocr/web_app.py flask run --host=0.0.0.0
        rm __init__.pyc; FLASK_APP=__init__.py flask run --host=0.0.0.0
push docker image
        sudo docker build -t oferyehuda/ocr .
        sudo docker login
        sudo docker push oferyehuda/ocr

Build flask docker
    docker build -t flask-sample-hello:latest .
    #docker run -d -p 5000:5000 flask-sample-hello

Building application from python
    follow this procedure - http://flask.pocoo.org/docs/0.12/patterns/packages/
    create setup.py
    run from setup.py folder - pip install -e .

POST - upload file to OCT
run another CMD window
vagrant ssh
curl -F file=@screenshots/Error2.jpg http://127.0.0.1:8080/api1/ocr
curl -F file=@screenshots/Error2.jpg http://127.0.0.1:8080/api1/ocr
curl http://127.0.0.1:8080/
curl -F file=@screenshots/error6.png https://ocrapi.cfapps.eu10.hana.ondemand.com/api1/ocr
curl -F file=@screenshots/error6.png https://ocrdev.cfapps.eu10.hana.ondemand.com/api1/ocr
ocrdev.cfapps.eu10.hana.ondemand.com

TESTING
python3 -m pytest test_ocr.py::TestOcr::test_cfocr
other tests might fail

RUN python3 /vagrant/get-pip.py
RUN pip install Flask
EXPOSE 5000

Cloud Foundry

cf login
cf apps
cf push ocrapi -b https://github.com/LeoKotschenreuther/python-tesseract-buildpack
cf push ocrdev -b https://github.com/ofer-yehuda/python-tesseract-buildpack
cf push ocrdev -b https://github.com/ofer-yehuda/python-buildpack-tesseract4
cf push ocrdev -b https://github.com/robertofalk/python-buildpack-tesseract4
cf v3-push ocrdev \ -b https://github.com/cloudfoundry/apt-buildpack -b https://github.com/cloudfoundry/python-buildpack

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## URLs

https://github.com/tesseract-ocr/tesseract/wiki/4.0-Docker-Containers
https://hub.docker.com/r/tesseractshadow/tesseract4re/
https://code-maven.com/docker
https://edumaven.com/python-programming/

AyTee test platform
https://itsdpphome-wb02ccf20.dispatcher.int.sap.hana.ondemand.com/webapp/index.html

SAP ML API's

OCR - https://api.sap.com/shell/discover/contentpackage/SAPLeonardoMLFunctionalServices/api/ocr_api?resource=OCR&operation=post_ocr
List of APIs - https://api.sap.com/shell/discover/contentpackage/SAPLeonardoMLFunctionalServices?section=ARTIFACTS

Create RESTApi with Flask
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

Flask
    welcome
    http://flask.pocoo.org/
    Quickstart
    http://flask.pocoo.org/docs/0.12/quickstart/#url-building
    large applications
        http://flask.pocoo.org/docs/0.12/patterns/packages/ 
        https://flask-restful.readthedocs.io/en/latest/
    Flask recieve files
        http://www.patricksoftwareblog.com/receiving-files-with-a-flask-rest-api/

SAP Cloud Foundery flask
https://blogs.sap.com/2017/12/04/deploying-flaskbottle-python-app-rest-api-on-sap-cloud-foundry/

SAP CF CLI
cf logon
cf target -o "I025026trial_OYTrail" -s "webocr"

tesseract

tesseract screenshots/Error3.jpg stdout -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz -psm 6

AyTee18 ENV:
vagrant provision
vagrant provision --provision-with=ayteeOCR
vagrant ssh -c "sudo docker restart ayteeOCR"
