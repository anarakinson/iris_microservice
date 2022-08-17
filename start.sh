#!/bin/bash


redis-server &
rq worker prediction_api 2>&1 | tee -a &
gunicorn prediction_api:app --preload -b 0.0.0.0:5000 --workers=2 2>&1 | tee -a
