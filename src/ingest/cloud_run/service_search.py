import uuid

from fastapi import UploadFile

from src.ingest.clients.gcs import GCSClient
from src.ingest.clients.vertex import VertexClient
from src.ingest.clients.bq import BigQueryClient


class SearchService:

    def __init__(self):

        self.gcs = GCSClient()
        self.vertex = VertexClient()
        self.bq = BigQueryClient()


    async def search_image(self, file: UploadFile):

        image_bytes = await file.read()

        image_name = str(uuid.uuid4())

        gcs_path = self.gcs.upload_image(
            folder="temp",
            nasa_id=image_name,
            image_bytes=image_bytes,
            content_type=file.content_type
        )

        embedding = self.vertex.generate_image_embedding(
            gcs_path
        )

        results = self.bq.search_similar_images(
            embedding
        )

        return {
            "status": "SUCCESS",
            "total_matches": len(results),
            "matches": results
        }