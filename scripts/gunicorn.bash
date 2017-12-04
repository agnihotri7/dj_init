#!/bin/bash

# Name of the application
NAME="dj_init"

# Django project directory
DJANGODIR=/home/dj_init.com/dj_init/dj_init

# The user to run as
USER=dj_init

# The group to run as
GROUP=dj_init

# How many worker processes should Gunicorn spawn
NUM_WORKERS=8

# Which settings file should Django use
DJANGO_SETTINGS_MODULE=config.local

# WSGI module name
DJANGO_WSGI_MODULE=config.wsgi

# Access logs
ACCESS_LOG='/home/dj_init.com/dj_init/dj_init/tmp/logs/access.log'

# Error logs
ERROR_LOG='/home/dj_init.com/dj_init/dj_init/tmp/logs/error.log'

# Log Level
LOG_LEVEL=debug # Options are debug, info, warning, error, critical

# Socket File to bind to
SOCKFILE=/home/dj_init.com/dj_init/dj_init/tmp/sockets/gunicorn.sock

################################# END OF CONFIGURATIONS #################################

# Change to project directory
cd $DJANGODIR

# Activate the virtual environment
source env/bin/activate

# Activate project environment
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn $DJANGO_WSGI_MODULE:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=$LOG_LEVEL \
  --bind=unix:$SOCKFILE \
  --access-logfile $ACCESS_LOG \
  --error-logfile $ERROR_LOG
