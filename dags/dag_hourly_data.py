import os
import pandas as pd
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine

from src.pipeline.extraction import DataExtraction
from src.pipeline.transformation import DataTransformation

from src.settings.config import user, password, host, port, database, RAW_PATH, PROCESSED_PATH

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

default_args={
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def extract_hourly(**context):
    pipeline_data_extraction = DataExtraction()
    raw_hourly_data = pipeline_data_extraction.get_hourly_data()

    raw_hourly_data.to_csv(f'{RAW_PATH}/hourly.csv', index=False)

    return pipeline_data_extraction.id

def transform_hourly(**context):
    location_id = context["ti"].xcom_pull(
        task_ids="data_extraction"
    )

    raw_hourly_data = pd.read_csv(f'{RAW_PATH}/hourly.csv')

    data_transformation = DataTransformation(location_id=location_id)
    transformed_hourly_data = data_transformation.transform_hourly_data(raw_hourly_data)

    transformed_hourly_data.to_csv(f'{PROCESSED_PATH}/hourly.csv', index=False)

def load_hourly():

    transformed_hourly_data = pd.read_csv(f'{PROCESSED_PATH}/hourly.csv')

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    transformed_hourly_data.to_sql(
        name='facthourlydata',
        con=engine,
        if_exists='replace',
        index=False
    )


with DAG(
    dag_id='hourly_data',
    default_args=default_args,
    description='Hourly moon/climate data - ETL',
    start_date=datetime(2026, 6, 12),
    schedule='@hourly',
    catchup=False,
) as dag:
    
    task_extract = PythonOperator(
        task_id='data_extraction',
        python_callable=extract_hourly
    )
    
    task_transform = PythonOperator(
        task_id='data_transformation',
        python_callable=transform_hourly
    )
    
    task_load = PythonOperator(
        task_id='data_loading',
        python_callable=load_hourly
    )

    task_extract >> task_transform >> task_load