#!/bin/bash

run_rq() {
  rq worker prediction_api -u 'redis://app-redis:6379' 2>&1 | tee -a &
}

run_gunicorn() {
  gunicorn prediction_api:app -b 127.0.0.1:5000  --preload --workers=2 2>&1 | tee -a 
}

run_rq
run_gunicorn
