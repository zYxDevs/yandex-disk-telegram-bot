#!/bin/bash

if [ "$1" = "flask" ]; then
  flask run
elif [ "$1" = "gunicorn" ]; then
  gunicorn --config ./src/configs/gunicorn.py wsgi:app
else
  echo "Invalid server name"
fi
