#%% Setup
from pyspark.ml.classification import LinearSVC
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import functions as f
import numpy as np
import pdb

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

features = [
    "tcp-srcport",
    "frame-len",
    "tcp-flags-push",
    "ip-flags-df",
    "Bytes"
    ]

df = spark.read.format("csv").option("header", "true").load("APA-DDoS-Dataset.csv")
for x in features:
    df = df.withColumn(x,f.col(x).cast("integer"))
    
#%% Modell Training
df = df.withColumn("label", (f.col("label") == "Benign").cast("int"))

assembler = VectorAssembler(inputCols=features, outputCol="features")
df = assembler.transform(df)
cl = LinearSVC()
model = cl.fit(df)
model.transform(df)
# %% Confidence Levels 
confidence = []
length = len(df.toPandas())
for i in range (0,1000):
    try:
        random = np.random.randint(1,length)
        row = df.rdd.take(random).pop().asDict()["features"]
        conf = model.predictRaw(row)
        diff = abs(conf[0]-conf[1])
        print(diff)
        confidence.append(diff)
    except:
        pass
# %%
import matplotlib.pyplot as plt
from scipy.stats import kde
density = kde.gaussian_kde(confidence)
x = np.linspace(0,5,100)
y=density(x)
plt.plot(x,y)
plt.title("Density Plot of the data")
plt.show()
# %%
