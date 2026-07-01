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