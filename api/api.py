from flask import Flask, request, Response
from pyspark.ml.classification import NaiveBayes,NaiveBayesModel
import json
import pdb
from classify import train,load,predict,get_context
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel

app = Flask(__name__)
global spark 

@app.before_first_request
def spark_session():
    get_context()
    try:
        load()
    except:
        train()

@app.route("/retrain")
def retrain():
    try:
        train()
        return Response(status=200)
    except: 
        return Response(status=500)

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(force=True)
    pred = predict(data)
    return 'Benign' if pred == 0 else 'DDos'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
