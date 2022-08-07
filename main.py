import os
import sys
from flask import Flask, jsonify, abort, make_response, request
import json
import requests
import time
import pandas as pd

import model as Model

###
# Application
app = Flask(__name__)


###
# model
model = Model.load_model()
# print(model)
targets = ['setosa', 'versicolor', 'virginica']


###
# model functions
def get_pred(sepal_length, sepal_width, petal_length, petal_width):
    columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    data = [sepal_length, sepal_width, petal_length, petal_width]
    print(data)
    df = pd.DataFrame([data], columns=columns)
    df = df.astype("float")
    pred = model.predict_proba(df)
    pred_round = [f"{elem : .3f}" for elem in pred[0]]
    out = pd.concat([pd.Series(targets), pd.Series(pred_round)], axis=1)
    out.columns = ["class", "probability"]
    return out


def launch_task(sepal_length, sepal_width, petal_length, petal_width, api):

    print("\n\n\n\n")
    print(f"{sepal_length=}", f"{sepal_width=}", f"{petal_length=}", f"{petal_width=}", f"{api=}")

    pred = get_pred(sepal_length, sepal_width, petal_length, petal_width)
    print(pred)

    if api == "v1.0":
        res_dict = {'result':  json.loads(pd.DataFrame(pred).to_json(orient='records'))}
    else:
        res_dict = {"Error" : "API does not exists"}

    return res_dict


###
# app functions
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


###
# errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"code" : "PAGE_NOT_FOUND"}), 404)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({"code" : "INTERNAL_SERVER_ERROR"}), 500)



if __name__ == "__main__":
    app.run(port=5050, debug=True)
