#!/bin/bash

run_rq() {
  rq worker prediction_api -u 'redis://app-redis:6379' 2>&1 | tee -a &
}

run_gunicorn() {
  gunicorn prediction_api:app --preload -b 0.0.0.0:5000 --workers=2 2>&1 | tee -a
}

run_rq
run_gunicorn
# python3 prediction_api.py
