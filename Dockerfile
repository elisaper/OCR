FROM tesseractshadow/tesseract4re

RUN apt-get update &&\
     apt-get -y upgrade &&\
     apt-get install -y python3-pip &&\
     apt-get install -y python-dev build-essential &&\
     apt-get install -y python3-pytest &&\
     apt-get install -y python3-requests &&\
     apt-get install -y git &&\
     apt-get install -y python-imaging
RUN  pip3 install Flask &&\
     pip3 install flask-cors &&\
     pip3 install pillow &&\
     pip3 install cfenv &&\
     pip3 install fuzzywuzzy
#    apt-get install -y curl &&\
#    apt-get install -y iputils-ping &&\
#    apt-get install net-tools &&\
#    apt-get install -y python3-pytest &&\
#    apt-get install -y python3-requests &&\
#    apt-get install -y python3-pip python-dev build-essential &&\
#    apt-get install -y python3-flask
#    apt-get update &&\
#    apt-get install -y git &&\
#    apt-get install -y python-imaging
#    apt-get update
#    apt-get install -y python-pip python-dev build-essential &&\
#RUN pip install --upgrade pip &&\
#    pip install Flask
EXPOSE 8080
RUN mkdir /app
ADD . /app
WORKDIR /app/
ENV FLASK_APP=__init.py__ LC_ALL=C.UTF-8 LANG=C.UTF-8
CMD FLASK_APP=ocr/web_app.py flask run --host=0.0.0.0 --port=8080
