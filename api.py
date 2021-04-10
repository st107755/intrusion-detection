from flask import Flask, request, Response
from flask_expects_json import expects_json
from sqlalchemy import create_engine
from pyspark.ml.classification import NaiveBayes,NaiveBayesModel
from sqlalchemy.orm import sessionmaker
import json
import pdb
import log
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

@app.route("/add", methods=["PUT"])
def add():
    try:
        engine = create_engine("postgresql://admin:qwe123@localhost:5432/ddos", echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        data = request.data
        json_data = json.loads(data)
        l = log.Log(tcp_srcport=2611,frame_len=54,tcp_flags_push=1,ip_flags_df=0,byte=648,label="DDoS-PSH-ACK")
        session.add(l)
        session.commit()
        return Response(status=201)
    except:
        return Response(status=422)

app.run(host="0.0.0.0", port=8080, debug=True)
