from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

default_args = {
    "owner": "aditya",
    "retries": 2,
}

with DAG(
    dag_id="nasa_ingestion_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["nasa", "cloud-run"],
) as dag:

    ingest = HttpOperator(
        task_id="trigger_ingestion",

        http_conn_id="cloud_run_ingest",

        endpoint="/ingest",

        method="POST",

        headers={
            "Content-Type": "application/json"
        },

        log_response=True,
    )

    deduplicate = BigQueryInsertJobOperator(
        task_id="remove_duplicates",

        configuration={
            "query": {
                "query": 
                """CREATE OR REPLACE TABLE `project-93d607b2-8e1c-46a9-893.INGEST_DATASET.INGEST_TABLE`
                        AS

                        SELECT * EXCEPT(rn)

                        FROM (

                            SELECT *,
                                ROW_NUMBER() OVER (
                                    PARTITION BY nasa_id
                                    ORDER BY date_created DESC
                                ) AS rn

                            FROM `project-93d607b2-8e1c-46a9-893.INGEST_DATASET.INGEST_TABLE`

                        )

                        WHERE rn = 1;
                                    """,
                                    "useLegacySql": False,
            }
        },
    )
    
    ingest >> deduplicate 