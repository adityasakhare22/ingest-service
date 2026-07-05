import os
from google.cloud import bigquery


class BigQueryClient:

    def __init__(self):

        self.client = bigquery.Client(
            project=os.environ["PROJECT_ID"]
        )

        project_id = os.environ["PROJECT_ID"]
        dataset = os.environ["BQ_DATASET"]
        table = os.environ["BQ_TABLE"]

        self.table_id = f"{project_id}.{dataset}.{table}"

    def insert_rows(self, rows: list) -> int:

        errors = self.client.insert_rows_json(
            self.table_id,
            rows
        )

        if errors:
            raise RuntimeError(
                f"Failed to insert rows into BigQuery: {errors}"
            )

        return len(rows)
    
    def search_similar_images(self, embedding):

        query = f"""
        SELECT
            base.nasa_id,
            base.title,
            base.description,
            base.image_url,
            base.gcs_image_path,
            distance
        FROM VECTOR_SEARCH(
            TABLE `{self.table_id}`,
            'image_embedding',
            (
                SELECT @embedding AS image_embedding
            ),
            top_k => 5
        )
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter(
                    "embedding",
                    "FLOAT64",
                    embedding
                )
            ]
        )

        query_job = self.client.query(
            query,
            job_config=job_config
        )

        return [dict(row) for row in query_job.result()]