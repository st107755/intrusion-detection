import pdb
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.sql import functions as f


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
features = ["ip-proto"]
df = df.withColumn("label", (f.col("label") == "Benign").cast("int"))
assembler = VectorAssembler(inputCols=features,outputCol="features")
df = assembler.transform(df)

### Classification ###
lr = LogisticRegression(maxIter=10)
model = lr.fit(df)
model.transform(df).show()

pdb.set_trace()