import requests
from datetime import datetime
import os
from src.ingest.clients.bq import BigQueryClient

NASA_URL = "https://images-api.nasa.gov/search"


class IngestService:

    def __init__(self):
        self.bq_client = BigQueryClient()

    def ingest_data(self):

        nasa_items = self.fetch_nasa_images("mars")

        rows = self.transform(nasa_items)

        inserted = self.bq_client.insert_rows(rows)

        return {
            "status": "SUCCESS",
            "rows_inserted": inserted
        }

    def fetch_nasa_images(self, query):
        #api_key = os.environ["NASA_API_KEY"]
        params = {
            "q": query,
            "media_type": "image"
        }

        response = requests.get(
            NASA_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()["collection"]["items"]

    def transform(self, items):

        rows = []

        for item in items:

            data = item["data"][0]

            links = item.get("links", [])

            image_url = None

            if links:
                image_url = links[0].get("href")

            rows.append(
                {
                    "nasa_id": data.get("nasa_id"),
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "keywords": ",".join(data.get("keywords", [])),
                    "media_type": data.get("media_type"),
                    "image_url": image_url,
                    "date_created": data.get("date_created")
                    #"ingestion_time": datetime.utcnow().isoformat()
                }
            )

        return rows


ingest_service = IngestService()