import json
from google.cloud import storage
import os

class GCSClient:

    def __init__(self):
        self.client = storage.Client(project=os.environ["PROJECT_ID"])
        self.bucket = self.client.bucket(os.environ["GCS_BUCKET"])

    def upload_json(self, filename, data):

        blob = self.bucket.blob(filename)
        
        if blob.exists():
            return f"gs://{self.bucket.name}/{filename}"
        else:
            blob.upload_from_string(
                json.dumps(data),
                content_type="application/json"
            )

        return f"gs://{self.bucket.name}/{filename}"


    def upload_image(self,
                     nasa_id,
                     folder,
                     image_bytes,
                     content_type="image/jpeg"):

        blob = self.bucket.blob(
               f"images/{folder}/{nasa_id}.jpg")

        if blob.exists():
            return f"gs://{self.bucket.name}/images/{folder}/{nasa_id}.jpg"
        else:
            
            blob.upload_from_string(
            image_bytes,
            content_type=content_type
        )

        return f"gs://{self.bucket.name}/images/{folder}/{nasa_id}.jpg"