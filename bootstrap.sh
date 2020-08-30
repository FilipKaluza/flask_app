
# fix annoying locale issue
echo 'export LC_ALL="en_US.UTF-8"' >> /home/vagrant/.bashrc
sed -i '/AcceptEnv/s/^#*/#/' /etc/ssh/sshd_config

#install Python 3.6
apt-get install software-properties-common
apt-get-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.6

#update alternatives
update-alternatives --instal /usr/bin/python3 python3 /usr/bin/python3.5 1
update-alternatives --instal /usr/bin/python3 python3 /usr/bin/python3.6 2

#install other dev tools
apt-get install -y git python-dev

#install pip lastest version
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

#install virtualenv
pip install virtualenv


