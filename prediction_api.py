import os
import sys

from flask import Flask, jsonify, abort, make_response, request
import json
import requests
import time
import copy
import pandas as pd

import logging
#
from rq import Queue, get_current_job
from rq.job import Job
from redis import Redis

import model as Model


###
# Queue
###
redis_conn = Redis(host="127.0.0.1", port=6379)
queue = Queue("prediction_api", connection=redis_conn, default_timeout=1200)


###
# logging
###
if not os.path.exists("logs"):
    os.mkdir("logs")
logging.basicConfig(filename="logs/logs.log", level=logging.DEBUG)


###
# Application
###
app = Flask(__name__)


###
# model
###
model = Model.load_model()
targets = Model.TARGETS


###
# queue function
###
def launch_task(data, api, job_id):
    '''
    Function to put prediction task to queue
    '''
    job = get_current_job()

    pred = Model.get_pred(model, data)

    if api == "v1.0":
        logging.info('[LAUNCH TASK]')
        res_dict = {'result':  json.loads(pd.DataFrame(pred).to_json(orient='records'))}
    else:
        logging.warning('[API DOES NOT EXISTS]')
        res_dict = {"Error" : "API does not exists"}

    return res_dict

def get_response(dict, status=200):
    return make_response(jsonify(dict), status)

def get_job_response(job_id):
    return get_response({"job_id" : job_id})

###
# app functions
###
@app.route('/iris/api/v1.0/getpred', methods=["GET"])
def get_task():
    '''
    Function to parse request and create task in queue
    '''
    job_id = request.args.get("job_id")

    data = {
        "sepal_length" : request.args.get("sepal_length"),
        "sepal_width" : request.args.get("sepal_width"),
        "petal_length" : request.args.get("petal_length"),
        "petal_width" : request.args.get("petal_width"),
    }

    job = queue.enqueue(
        "prediction_api.launch_task",
        data,
        "v1.0",
        job_id,
        result_ttl=(60 * 60 * 24),
        job_id=job_id,
        job_timeout=600,
    )

    return get_job_response(job.get_id())


def get_process_response(code, process_status, status=200):
    response = {
        "CODE" : code,
        "STATUS" : process_status
    }
    return get_response(response, status)

@app.route("/iris/api/v1.0/status/<job_id>")
def status(job_id):
    '''
    Function returns status of task
    '''
    job = queue.fetch_job(job_id)

    if job is None:
        return get_process_response("NOT_FOUND", "error", 404)

    if job.is_failed:
        return get_process_response("INTERNAL_SERVER_ERROR", "error", 500)

    if job.is_finished:
        return get_process_response("READY", "success")

    return get_process_response("NOT_READY", "running", 202)


@app.route("/iris/api/v1.0/result/<job_id>")
def result(job_id):
    '''
    Function to get result of model prediction from queue
    '''
    job = queue.fetch_job(job_id)

    if job is None:
        return get_process_response("NOT_FOUND", "error", 404)

    if job.is_failed:
        return get_process_response("INTERNAL_SERVER_ERROR", "error", 500)

    if job.is_finished:
        job_result = copy.deepcopy(job.result)
        result = {
            "result": job_result["result"]
        }

        return get_response(result)

    return get_process_response("NOT_FOUND", "error", 404)


###
# errors
###
@app.errorhandler(404)
def not_found(error):
    logging.warning('[PAGE_NOT_FOUND]')
    return make_response(jsonify({"code" : "PAGE_NOT_FOUND"}), 404)

@app.errorhandler(500)
def server_error(error):
    logging.warning('[INTERNAL_SERVER_ERROR]')
    return make_response(jsonify({"code" : "INTERNAL_SERVER_ERROR"}), 500)



if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as ex:
        logging.debug(f'[APPLICATION_ERROR]: {ex}')
