#!/bin/bash

cd /home/pi/desarrollo/python/flask/actuador

export FLASK_APP=test
export FLASK_DEBUG=1

flask run --host=10.68.0.101 --port=5000
