#!/bin/bash

run_gunicorn() {
  gunicorn prediction_api:app --preload -b 127.0.0.1:5000 --workers=2 2>&1 | tee -a
}

run_gunicorn
