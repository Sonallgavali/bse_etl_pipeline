from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime
import subprocess


# Function to run ETL script
def run_loader():

    subprocess.run(
        ['python', '/opt/airflow/scripts/load_bhavcopy.py'],
        check=True
    )


# Default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 5, 1),
    'retries': 1
}


# DAG definition
with DAG(
    dag_id='bse_bhavcopy_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='BSE BhavCopy ETL Pipeline'
) as dag:

    # Task 1 - Load CSV data
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=run_loader
    )

    # Task 2 - Transform data
    transform_data = PostgresOperator(
        task_id='transform_data',
        postgres_conn_id='postgres_default',
        sql="""

        INSERT INTO fact_stock_prices (
            symbol,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            avg_close_last_3_days
        )

        SELECT
            symbol,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,

            AVG(close_price) OVER (
                PARTITION BY symbol
                ORDER BY trade_date
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) AS avg_close_last_3_days

        FROM stg_bhavcopy;

        """
    )

        # Task 3 - Audit logging
    audit_logging = PostgresOperator(
        task_id='audit_logging',
        postgres_conn_id='postgres_default',
        sql="""

        INSERT INTO etl_audit_log (
            job_name,
            source_file,
            records_loaded,
            status,
            start_time,
            end_time
        )

        VALUES (
            'bse_bhavcopy_etl_pipeline',
            'multiple_csv_files',
            (SELECT COUNT(*) FROM fact_stock_prices),
            'SUCCESS',
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        );

        """
    )

    # Task flow
    load_data >> transform_data >> audit_logging
