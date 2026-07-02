import uuid

from fastapi import UploadFile

from src.ingest.clients.gcs import GCSClient
from src.ingest.clients.vertex import VertexClient


class SearchService:

    def __init__(self):
        self.gcs = GCSClient()
        self.vertex = VertexClient()

    async def search_image(self, file: UploadFile):

        # Read uploaded image
        image_bytes = await file.read()

        # Generate unique filename
        image_name = f"{uuid.uuid4()}.jpg"

        # Upload to GCS
        gcs_path = self.gcs.upload_image(
            folder="temp",
            nasa_id=image_name.replace(".jpg", ""),
            image_bytes=image_bytes,
            content_type=file.content_type
        )

        # Generate image embedding
        embedding = self.vertex.generate_image_embedding(gcs_path)

        # Temporary response
        return {
            "status": "SUCCESS",
            "filename": image_name,
            "gcs_path": gcs_path,
            "embedding_dimensions": len(embedding)
        }