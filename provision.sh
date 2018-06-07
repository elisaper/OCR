#!/bin/bash
NAME="watson"
PKGS="python-pip docker.io"
for PKG in $PKGS
do
	dpkg -V $PKG || { 
		apt-get -y update
		apt-get -y install $PKGS
	}
done
#pip install --upgrade watson-developer-cloud
cd /vagrant
#docker build -t ocr .
#docker run -it -p 5000:5000 -v $(pwd):/opt ocr
cd /opt



