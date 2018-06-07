# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.define "ocr" do |ocr|
    ocr.vm.box = "bento/ubuntu-16.04"
    #ocr.vm.network "private_network", ip: "192.168.57.10"
    ocr.vm.network "forwarded_port", guest: 8080, host: 8080
    ocr.vm.provision "shell", path: "provision.sh"
  end
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2096"]
  end
end
