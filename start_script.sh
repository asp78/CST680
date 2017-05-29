#!/bin/bash

virtualenv env
source ./env/bin/activate
pip install -r requirements.txt

#export FLASK_APP=app.py
#flask run --host=0.0.0.0
python app.py
