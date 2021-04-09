import pandas as pd
import pdb

df = pd.read_csv("APA-DDoS-Dataset.csv")
#### Not Floatable
df = df = df.drop(columns=["ip.src", "ip.dst"])
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
### Clean Up
df["frame.time"] = df["frame.time"].apply(
    lambda x: x.replace("Mountain Daylight Time", "")
)
df["frame.time"] = df[
    df["frame.time"] != " 16-Jun 2020 20:18:15.07416-Jun 202000 Mountain Daylight Time"
]
df["frame.time"] = df["frame.time"].astype("datetime64")
df = df.rename(columns = {'Bytes':'byte'})
df.columns = [c.lower() for c in df.columns]  # postgres doesn't like capitals or spaces
df.columns = [c.replace(".", "_") for c in df.columns]


from sqlalchemy import create_engine

engine = create_engine("postgresql://admin:qwe123@localhost:5432/ddos")

df.to_sql("ddos", con=engine, if_exists="replace", schema="public",index=False)
with engine.connect() as con:
    con.execute('ALTER TABLE ddos ADD COLUMN id SERIAL PRIMARY KEY;')
