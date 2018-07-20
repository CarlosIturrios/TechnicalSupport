# How to install TechnicalSupport
Install python version 2.7
## Clone git repository
`git clone https://github.com/CarlosIturrios/TechnicalSupport.git`
## Install virtualenv library
`pip install virtualenv`
## Create new virtualenv
`virtualenv env`
## Activate virtualenv
Windows `env\Scripts\activate`
Linux/MacOs `source env/bin/activate`
## Install requirements.txt
`pip install -r requirements.txt`
## Create Database
`python manage.py`
## How to create user
`python manage.py createsuperuser`
## Run Project
python manage.py runserver
## Desactivar virtualenv
`deactivate`
