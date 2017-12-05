#!/bin/bash
#Find and replace project name
pwd
echo "Hello, whare is project located?"
read project_dir
echo "what is your old project name?"
read old_project_name
echo "what is your new project name?"
read new_project_name

cd $project_dir
echo "cleaning .pyc files"
find . -type f -name "*.pyc" | xargs rm -rf
echo "renaming project name"
mv $old_project_name $new_project_name
cd $new_project_name
mv $old_project_name $new_project_name

echo "updating config file names to new proj name"
mv config/nginx/"$old_project_name".conf config/nginx/"$new_project_name".conf
mv config/nginx/"$old_project_name"-ssl.conf config/nginx/"$new_project_name"-ssl.conf
mv config/supervisor/"$old_project_name".conf config/supervisor/"$new_project_name".conf
mv config/supervisor/"$old_project_name"_celery.conf config/supervisor/"$new_project_name"_celery.conf
mv config/supervisor/"$old_project_name"_celerybeat.conf config/supervisor/"$new_project_name"_celerybeat.conf

echo "updating project name in config files"
grep -rli $old_project_name * | xargs -i@ sed -i "s/$old_project_name/$new_project_name/g" @

echo "cerating local.py settings file"
cp config/local.py.example config/local.py
echo "New project is setup successfully as $new_project_name"

echo "creating virtual env and installing requirements.txt"
virtualenv -p /usr/bin/python3.5 env
source env/bin/activate
pip install -r requirements.txt

echo "applying migrations ..."
python manage.py migrate

echo "creating super user ..."
python manage.py createsuperuser
