#!/bin/bash

cd /home/pi/desarrollo/python/flask/webActuador

export FLASK_APP=domoticae
export FLASK_DEBUG=1

flask run --host=10.68.1.2 --port=5000
