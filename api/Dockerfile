FROM openjdk:8
ENV PYTHONPATH /usr/bin/python3
COPY classify.py .
COPY api.py .
COPY log.py .
COPY postgresql-42.2.19.jar .
RUN apt update 
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y libpq-dev
RUN pip3 install Flask
RUN pip3 install pyspark
RUN pip3 install pandas 
RUN pip3 install sqlalchemy
RUN pip3 install psycopg2
RUN pip3 install gunicorn
EXPOSE 8000
CMD gunicorn -w 4 --bind 0.0.0.0:8000 api:app