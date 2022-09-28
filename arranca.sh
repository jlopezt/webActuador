#!/bin/bash

cd /home/pi/desarrollo/python/flask/actuador

export FLASK_APP=test
export FLASK_ENV=development

flask run --host=10.68.0.101
