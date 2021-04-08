#%%
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import pdb
from pandas_profiling import ProfileReport
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("APA-DDoS-Dataset.csv")
#### Not Floatable
label = df["Label"]
df = df.drop(columns=["ip.src", "ip.dst", "frame.time", "Label"])
#### Constant
df = df.drop(
    columns=[
        "tcp.dstport",
        "ip.proto",
        "tcp.flags.syn",
        "tcp.flags.reset",
        "tcp.flags.ack",
        "ip.flags.mf",
        "ip.flags.rb",
        "tcp.seq",
        "tcp.ack",
    ]
)
#### High Correlation
df = df.drop(columns=["Tx Packets", "Tx Bytes", "Rx Packets", "Rx Bytes", "Packets"])
#%%
profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
profile.to_notebook_iframe()

# %%
X_train, X_test, y_train, y_test = train_test_split(df, label, test_size=0.33)
# clf = LogisticRegression(C=1e5)
# clf = MultinomialNB()
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
# %%
df.columns

# %%
