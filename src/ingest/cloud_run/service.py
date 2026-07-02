import requests
from datetime import datetime
import os
from src.ingest.clients.bq import BigQueryClient
from src.ingest.clients.gcs import GCSClient

NASA_URL = "https://images-api.nasa.gov/search"


class IngestService:

    def __init__(self):
        self.bq_client = BigQueryClient()
        self.gcs = GCSClient()

    def fetch_nasa(self, search_term):

        response = requests.get(
            NASA_URL,
            params={
                "q": search_term,
                "media_type": "image"
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    
    def ingest_data(self):

        total_rows = 0
        total_images = 0
        SEARCH_TERMS = ["mercury","venus","earth","moon","mars","jupiter","saturn","uranus","neptune","pluto"]
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")


        for search_term in SEARCH_TERMS:

            print(f"Ingesting {search_term}")

            raw_json = self.fetch_nasa(search_term)
            
            self.gcs.upload_json(
                filename = f"raw/{search_term}/{timestamp}.json",
                data=raw_json
            )

            items = raw_json["collection"]["items"][:20]

            self.download_images(search_term, items)

            rows = self.transform(items)

            inserted = self.bq_client.insert_rows(rows)

            total_rows += inserted
            total_images += len(items)

        return {
            "status": "SUCCESS",
            "queries_processed": len(SEARCH_TERMS),
            "images_processed": total_images,
            "rows_inserted": total_rows
        }

    def download_images(self, search_term, items):

        for item in items:

            data = item["data"][0]

            links = item.get("links", [])

            if not links:
                continue

            image_url = links[0]["href"]

            image_response = requests.get(
                image_url,
                timeout=30
            )

            image_response.raise_for_status()

            self.gcs.upload_image(
        folder=search_term,
        nasa_id=data["nasa_id"],
        image_bytes=image_response.content,
        content_type=image_response.headers.get(
            "Content-Type",
            "image/jpeg"
    )
)
            


    def transform(self, items):

        rows = []

        for item in items:

            data = item["data"][0]

            links = item.get("links", [])

            image_url = links[0]["href"] if links else None

            rows.append({
                "nasa_id": data.get("nasa_id"),
                "title": data.get("title"),
                "description": data.get("description"),
                "keywords": ",".join(data.get("keywords", [])),
                "media_type": data.get("media_type"),
                "image_url": image_url,
                "date_created": data.get("date_created")
            })

        return rows


ingest_service = IngestService()