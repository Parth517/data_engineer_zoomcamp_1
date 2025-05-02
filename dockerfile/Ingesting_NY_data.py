import pandas as pd
import os
from sqlalchemy import create_engine
from time import time
import argparse

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db_name=params.db_name
    table_name=params.table_name
    url=params.url
    
    csv_name='output.csv'
    # download the csv
    os.system(f"curl -L {url} -o {csv_name}")
    
    df=pd.read_csv(csv_name,compression='gzip',nrows=100,low_memory=False)
    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    
    engine.connect()

    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

    df_iter=pd.read_csv(csv_name,iterator=True,chunksize=100000,compression= 'gzip',low_memory=False) 
    df=next(df_iter)

    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace') 

    while True:
        t_start=time()
        df=next(df_iter) 
        df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name,con=engine,if_exists='append')
        t_end=time()
        print('Inserted another chunck....,took %.3f seconds'%(t_end-t_start))
if __name__=='__main__':
    
    # create the parser
    # add arguments
    # user,
    # password,
    # host,
    # port,
    # db_name,
    # table_name,
    # url of the csv
    parser=argparse.ArgumentParser(description='Ingest NY taxi data')
    #user,
    parser.add_argument('--user',help='user name to connect to the database')
    # password,
    parser.add_argument('--password',help='password to connect to the database')  
    # host,
    parser.add_argument('--host',help='host name to connect to the database') 
    # port,
    parser.add_argument('--port',help='port to connect to the database')
    #db_name,
    parser.add_argument('--db_name',help='database name to connect to the database')
    # table_name,
    parser.add_argument('--table_name',help='table name to connect to the database')
    #url of the csv
    parser.add_argument('--url',help='url of the csv file to be ingested')


    args=parser.parse_args()
    main(args)


