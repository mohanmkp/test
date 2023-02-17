#!/bin/bash

if [ -d "venv" ]
then
    echo "PYTHON VIRTUAL ENVIRONMENT EXISTS."
else
    virtualenv -p python3.9 venv
fi

source venv/bin/activate

python3 manage.py makemigrations merge --noinput

python3 manage.py makemigrations --noinput

python3 manage.py migrate

python3 manage.py runserver