FROM debian:buster-slim
COPY sql-import.py .
COPY APA-DDoS-Dataset.csv .
RUN apt update 
RUN apt install -y wget 
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y libpq-dev
RUN pip3 install pandas 
RUN pip3 install sqlalchemy
RUN pip3 install psycopg2
CMD python3 sql-import.py arg

