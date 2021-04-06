import pandas as pd
df = pd.read_csv('APA-DDoS-Dataset.csv')
df.columns = [c.lower() for c in df.columns] #postgres doesn't like capitals or spaces

from sqlalchemy import create_engine
engine = create_engine('postgresql://admin:qwe123@localhost:5432/ddos')

df.to_sql("ddos-data", con=engine,if_exists='append',schema='public')