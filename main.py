import os
import sys
from flask import Flask, jsonify, abort, make_response, request
import json
import requests
import time


app = Flask(__name__)

def launch_task(sepal_length, sepal_width, petal_length, petal_width, api):

    print(f"{sepal_length=}", f"{sepal_width=}", f"{petal_length=}", f"{petal_width=}", f"{api=}")

    if api == "v1.0":
        res_dict = {"Done" : "API exists"}
    else:
        res_dict = {"Error" : "API does not exists"}

    return res_dict

@app.route('/iris/api/v1.0/getpred', methods=["GET"])
def get_task():
    result = launch_task(
        request.args.get("sepal_length"),
        request.args.get("sepal_width"),
        request.args.get("petal_length"),
        request.args.get("petal_width"),
        "v1.0",
    )

    return make_response(jsonify(result), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"code" : "PAGE_NOT_FOUND"}), 404)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({"code" : "INTERNAL_SERVER_ERROR"}), 500)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
