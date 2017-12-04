Dj_Init
=======

# Important Notes

This guide is long because it covers many cases and includes all commands you need.

This installation guide was created for and tested on **Ubuntu 16.04** operating systems.

This is the official installation guide to set up a production server. To set up a **development installation** and to contribute read `Contributing.md`.

The following steps have been known to work. Please **use caution when you deviate** from this guide. Make sure you don't violate any assumptions Dj_Init makes about its environment.

# Overview

The  Dj_Init installation consists of setting up the following components:

1. Packages / Dependencies
2. System Users
3. Database
4. Dj_Init
5. Supervisor
6. Nginx
7. Update Existing Setup to Newer Version

## Packages / Dependencies

Run following commands

    sudo apt-get update
    sudo apt-get -y upgrade

**Note:** To set VIM editor as default editor.

    # Install vim and set as default editor
    sudo apt-get install -y vim-gnome
    sudo update-alternatives --set editor /usr/bin/vim.gnome

Install the required packages (needed to compile Ruby and native extensions to Ruby gems):

    sudo apt-get install -y build-essential git-core libssl-dev libffi-dev curl redis-server checkinstall libcurl4-openssl-dev python-docutils pkg-config python3-dev python-dev python-virtualenv

**Note:** In order to receive mail notifications, make sure to install a mail server. The recommended mail server is postfix and you can install it with:

    sudo apt-get install -y postfix

Then select 'Internet Site' and press enter to confirm the hostname.

# System Users

Create a `dj_init` user for Dj_Init:

    sudo adduser --disabled-login --gecos 'Dj_Init' dj_init

# Database

We recommend using a PostgreSQL database.

    # Install the database packages
    sudo apt-get install -y postgresql postgresql-client libpq-dev

    # Login to PostgreSQL
    sudo -u postgres psql -d postgres

    # Create a user for Dj_Init
    # Do not type the 'postgres=#', this is part of the prompt
    postgres=# CREATE USER dj_init WITH PASSWORD '123456' CREATEDB;

    # Create the Dj_Init production database & grant all privileges on database
    postgres=# CREATE DATABASE dj_init_production OWNER dj_init;

    # Quit the database session
    postgres=# \q

    # Try connecting to the new database with the new user
    sudo -u dj_init -H psql -d dj_init_production

    # Quit the database session
    dj_init_production> \q

# Dj_Init

    # We'll install Dj_Init into home directory of the user "dj_init"
    cd /home/dj_init

## Clone the Source

    # Clone Dj_Init repository
    sudo -u dj_init -H dj_init clone https://github.com/dimusco/dj_init.git dj_init

## Configure It

    # Switch User dj_init
    sudo su dj_init

    # Go to Dj_Init installation folder
    cd /home/dj_init/dj_init

    # Virtual Envirnoment and requirements
    virtualenv -p /usr/bin/python3.5 env
    source env/bin/activate
    pip install -r requirements.txt

## Project and Database Configuartion Settings

    # Edit desired configurations in config/local.py i.e. STATICFILES_DIRS
    cp config/local.py.example config/local.py
    chmod o-rwx config/local.py
    editor config/local.py

Example:

        DEBUG = False

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'dj_init_production',
                'USER': 'dj_init',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '',
            }
        }

## Validate configurations

    ./manage.py validate

## Migrate Database & Seed Default Data

    ./manage.py migrate
    ./manage.py loaddata fixtures/default.json

## Load Assets

    ./manage.py collectstatic

## Gunicorn Or uWSGI

    # Copy either of the configuration file for respective server
    cp scripts/gunicorn.bash scripts/runserver.bash

    OR

    cp scripts/uwsgi.bash scripts/runserver.bash

    # Make it executable
    chmod u+x scripts/runserver.bash

## Celery & Celerybeat

    cp scripts/celery.bash.example scripts/celery.bash
    cp scripts/celerybeat.bash.example scripts/celerybeat.bash

## Exit User dj_init

    exit

# Supervisor

## Installation

    sudo apt-get install -y supervisor

    # Go to Dj_Init installation folder
    cd /home/dj_init/dj_init

## Configuration

    sudo cp config/supervisor/dj_init.conf /etc/supervisor/conf.d/dj_init.conf
    sudo cp config/supervisor/dj_init_celery.conf /etc/supervisor/conf.d/dj_init_celery.conf
    sudo cp config/supervisor/dj_init_celerybeat.conf /etc/supervisor/conf.d/dj_init_celerybeat.conf

## Supervisor Configuration Update

    sudo service supervisor restart
    sudo supervisorctl reread
    sudo supervisorctl update

# Nginx

## Installation

    sudo apt-get install -y nginx

## Site Configuration

    # Copy the example site config:
    sudo cp config/nginx/dj_init.cnf /etc/nginx/sites-available/dj_init.cnf
    sudo ln -s /etc/nginx/sites-available/dj_init.cnf /etc/nginx/sites-enabled/dj_init.cnf

Make sure to edit the config file to match your setup:

    # Change YOUR_SERVER_FQDN to the fully-qualified
    # domain name of your host serving Dj_Init.
    sudo editor /etc/nginx/sites-available/dj_init.cnf

**Note:** If you want to use HTTPS, replace the `dj_init` Nginx config with `dj_init-ssl`. See [Using HTTPS](#using-https) for HTTPS configuration details.

## Test Configuration

Validate your `dj_init` or `dj_init-ssl` Nginx config file with the following command:

    sudo nginx -t

You should receive `syntax is okay` and `test is successful` messages. If you receive errors check your `dj_init` or `dj_init-ssl` Nginx config file for typos, etc. as indicated in the error message given.

## Provide access to static files and error templates

    sudo adduser nginx dj_init
    sudo chmod -R 750 /home/dj_init/dj_init/static/
    sudo chmod -R 750 /home/dj_init/dj_init/templates/

## Restart

    sudo service nginx restart

# Update Existing Setup to Newer Version


# Using HTTPS

To use Dj_Init with HTTPS:


Using a self-signed certificate is discouraged but if you must use it follow the normal directions then:

1. Generate a self-signed SSL certificate:

    ```
    mkdir -p /etc/nginx/ssl/
    cd /etc/nginx/ssl/
    sudo openssl req -newkey rsa:2048 -x509 -nodes -days 3560 -out dj_init.crt -keyout dj_init.key
    sudo chmod o-r dj_init.key
    ```
