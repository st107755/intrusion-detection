import pdb
from pyspark.sql import SparkSession,Row
from pyspark.ml.classification import LogisticRegression, NaiveBayes, LinearSVC
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.mllib.regression import StreamingLinearRegressionWithSGD
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator
from pyspark.sql import functions as f
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from multiprocessing import Process
import pandas as pd
import log

modell = None 
spark = None 
session = None
features = [
    "tcp_srcport",
    "frame_len",
    "tcp_flags_push",
    "ip_flags_df",
    "byte"
    ]

def get_context():
    global spark
    global session
    ### Spark
    spark = (
        SparkSession.builder.appName("Python Spark SQL basic example")
        .config("spark.jars", "postgresql-42.2.19.jar")
        .config("spark.worker.timeout","420")
        .getOrCreate()
    )
    ### Database 
    engine = create_engine("postgresql://admin:qwe123@db:5432/ddos", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

def train():
    global spark
    df = (
        spark.read.format("jdbc")
        .option("url", "jdbc:postgresql://db:5432/ddos")
        .option("dbtable", "ddos")
        .option("user", "admin")
        .option("password", "qwe123")
        .option("driver", "org.postgresql.Driver")
        .load()
    )

    ### Pre Processing ###
    global features
    df = df.withColumn("label", (f.col("label") == "Benign").cast("int"))
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    df = assembler.transform(df)

    ### Classification ###
    cl = LinearSVC()
    cl.setRegParam(0.1)
    global model
    model = cl.fit(df)
    model.transform(df)
    model.write().overwrite().save("modell")

def load():
    global model 
    cl = NaiveBayes()
    model = cl.load("modell")

def add(data,prediction):
    label = 'Benign' if prediction == 0 else 'DDos'
    l = log.Log(data["tcp_srcport"],data["frame_len"],data["tcp_flags_push"],data["ip_flags_df"],data["byte"],label)
    session.add(l)
    session.commit()

def suitable_for_learning(confidence):
    confidence_factor = 2
    if abs(confidence[0]-confidence[1]) > confidence_factor:
        return True
    return False

def predict(data):
    global model
    values = list([tuple([int(x) for x in data.values()])])
    keys = [*data.keys()]
    df = spark.createDataFrame(values,keys)
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    df = assembler.transform(df)
    prediction = model.predict(df.head().features)
    ### Unsupervised Learning ###
    confidence = model.predictRaw(df.head().features)
    if suitable_for_learning(confidence):
        process = Process(  # Create a daemonic process with heavy "my_func"
        target=add(data,prediction),
        daemon=True
        )
        process.start()
    return prediction