FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY Ingesting_NY_data.py Ingesting_NY_data.py
ENTRYPOINT [ "python","Ingesting_NY_data.py" ]