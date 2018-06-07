#!/bin/bash

cd $BASEDIR
docker build -t aytee_ocr . 

docker rm -f ayteeOCR
docker run -d \
	--network=$PROJECT \
	--name ayteeOCR \
	-v $BASEDIR:/app \
	-p 0.0.0.0:8080:8080 \
	aytee_ocr

