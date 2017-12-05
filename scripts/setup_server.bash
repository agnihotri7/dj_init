#!/bin/bash
echo "Reading configurations ..."
source ../config/EC2/ec2_server.conf

echo "creating user $USERNAME"
sudo adduser --disabled-password $USERNAME
cd /home/"$USERNAME"
sudo -u $USERNAME mkdir "$PROJECT_NAME".com
cd "$PROJECT_NAME".com
sudo -u $USERNAME mkdir static
sudo -u $USERNAME mkdir media

echo "cloning project..."
sudo -u $USERNAME git clone $PROJECT_REPO $PROJECT_NAME
cd $PROJECT_NAME

echo "creating virtualenv with python 3.5 inside env dir and installing requirements..."
sudo -u $USERNAME virtualenv -p /usr/bin/python3.5 env
source env/bin/activate
pip install -r requirements.txt

echo "updating settings file a local.py..."
sudo -u $USERNAME cp config/local.py.example config/local.py

echo "applying migrations ..."
sudo -u $USERNAME python manage.py migrate

echo "creating super user ..."
sudo -u $USERNAME python manage.py createsuperuser

echo "using collectstatic ..."
sudo -u $USERNAME python manage.py collectstatic

echo "update system ..."
sudo -u root apt-get update

echo "install requirements ..."
# sudo -u root apt-get install git gcc python-dev python-setuptools python-virtualenv libjpeg-dev zlib1g-dev libpq-dev nginx supervisor postgresql postgresql-contrib

echo "add supervisor.conf ..."
sudo -u root cp config/"$PROJECT_NAME".conf /etc/supervisor/conf.d/"$PROJECT_NAME".conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status $PROJECT_NAME

echo "add nginx.conf ..."
sudo -u root vi /etc/nginx/sites-available/"$PROJECT_NAME".conf
sudo ln -s /etc/nginx/sites-available/"$PROJECT_NAME".conf /etc/nginx/sites-enabled/"$PROJECT_NAME".conf
sudo service nginx -t
sudo service nginx restart
