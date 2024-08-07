#!/bin/bash

export FLASK_ENV=production
venv/bin/gunicorn --config gunicorn_config.py app:server

