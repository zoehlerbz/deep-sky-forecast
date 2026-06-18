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

def extract_daily(**context):
    pipeline_data_extraction = DataExtraction()
    raw_daily_data = pipeline_data_extraction.get_daily_data()

    raw_daily_data.to_csv(f'{RAW_PATH}/daily.csv', index=False)

    return pipeline_data_extraction.id

def transform_daily(**context):
    location_id = context["ti"].xcom_pull(
        task_ids="data_extraction"
    )

    raw_daily_data = pd.read_csv(f'{RAW_PATH}/daily.csv')

    data_transformation = DataTransformation(location_id=location_id)
    transformed_daily_data = data_transformation.transform_daily_data(raw_daily_data)

    transformed_daily_data.to_csv(f'{PROCESSED_PATH}/daily.csv', index=False)

def load_daily():

    transformed_daily_data = pd.read_csv(f'{PROCESSED_PATH}/daily.csv')

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    transformed_daily_data.to_sql(
        name='factdailydata',
        con=engine,
        if_exists='replace',
        index=False
    )


with DAG(
    dag_id='daily_data',
    default_args=default_args,
    description='Daily moon data - ETL',
    start_date=datetime(2026, 6, 12),
    schedule='@hourly',
    catchup=False,
) as dag:
    
    task_extract = PythonOperator(
        task_id='data_extraction',
        python_callable=extract_daily
    )
    
    task_transform = PythonOperator(
        task_id='data_transformation',
        python_callable=transform_daily
    )
    
    task_load = PythonOperator(
        task_id='data_loading',
        python_callable=load_daily
    )

    task_extract >> task_transform >> task_load