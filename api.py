from flask import Flask, request, Response
from flask_expects_json import expects_json
from classify import train
from pyspark.ml.classification import LogisticRegression, NaiveBayes
import json
import pdb
from log import Log

app = Flask(__name__)


@app.route("/retrain")
def retrain():
    train()
    return Response(status=200)


@app.route("/classify", methods=["POST"])
def classify():
    data = request.data
    json_data = json.loads(data)
    pdb.set_trace()
    nb = NaiveBayes()
    nb.load("modell")
    nb

@app.route("/add", methods=["PUT"])
def add():
    o =  new Log()


app.run(host="0.0.0.0", port=8080, debug=True)
