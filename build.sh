#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py collectstatic --no-input
python manage.py migrate
pip install --upgrade pip
pip install --force-reinstall -U setuptools
pip install tensorflow
pip install pathlib
pip install numpy 
pip install opencv-python