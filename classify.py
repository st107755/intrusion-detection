import pdb
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression,NaiveBayes
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.mllib.regression import StreamingLinearRegressionWithSGD
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator
from pyspark.sql import functions as f

def train():
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.jars", "postgresql-42.2.19.jar") \
        .getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/ddos") \
        .option("dbtable", "data") \
        .option("user", "admin") \
        .option("password", "qwe123") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    ### Pre Processing ###
    train, test = df.randomSplit([0.8, 0.2], seed=42)
    features = ["ip-proto","frame-len","tcp-flags-syn","tcp-flags-reset","tcp-flags-push","tcp-flags-ack","ip-flags-mf","ip-flags-df","ip-flags-rb","tcp-seq","tcp-ack","packets","bytes","tx packets","tx bytes","rx packets","rx bytes"]
    df = train.withColumn("label", (f.col("label") == "Benign").cast("int"))
    assembler = VectorAssembler(inputCols=features,outputCol="features")
    df = assembler.transform(df)

    ### Classification ###
    cl = NaiveBayes()
    model = cl.fit(df)
    model.transform(df)
    model.write().overwrite().save("modell")