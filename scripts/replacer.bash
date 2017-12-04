#!/bin/bash
#Find and replace project name
echo "Hello, whare is project located?"
read project_dir
cd $project_dir
echo "what is your old project name?"
read old_project_name
echo "what is your new project name?"
read new_project_name
mv $old_project_name $new_project_name
cd $new_project_name
mv $old_project_name $new_project_name
grep -rli $old_project_name * | xargs -i@ sed -i "s/$old_project_name/$new_project_name/g" @
cp config/local.py.example config/local.py
echo "New project is setup successfully $new_project_name"

