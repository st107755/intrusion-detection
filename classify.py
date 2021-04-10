import pdb
from pyspark.sql import SparkSession,Row
from pyspark.ml.classification import LogisticRegression, NaiveBayes
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.mllib.regression import StreamingLinearRegressionWithSGD
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator
from pyspark.sql import functions as f
import pandas as pd

modell = None 
spark = None 
features = [
    "tcp_srcport",
    "frame_len",
    "tcp_flags_push",
    "ip_flags_df",
    "byte"
    ]

def get_context():
    global spark
    spark = (
        SparkSession.builder.appName("Python Spark SQL basic example")
        .config("spark.jars", "postgresql-42.2.19.jar")
        .getOrCreate()
    )

def train():
    global spark
    df = (
        spark.read.format("jdbc")
        .option("url", "jdbc:postgresql://localhost:5432/ddos")
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
    cl = NaiveBayes()
    global model
    model = cl.fit(df)
    model.transform(df)
    model.write().overwrite().save("modell")

def load():
    global model 
    cl = NaiveBayes()
    model = cl.load("modell")

def predict(data):
    global model
    values = list([tuple([int(x) for x in data.values()])])
    keys = [*data.keys()]
    df = spark.createDataFrame(values,keys)
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    df = assembler.transform(df)
    return model.predict(df.head().features)