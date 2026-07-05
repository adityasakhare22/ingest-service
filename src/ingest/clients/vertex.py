import os

import vertexai
from vertexai.vision_models import (Image,MultiModalEmbeddingModel)


class VertexClient:

    def __init__(self):

        vertexai.init(
            project=os.environ["PROJECT_ID"],
            location=os.environ["VERTEX_REGION"]
        )

        self.model = MultiModalEmbeddingModel.from_pretrained(
            "multimodalembedding@001"
        )

    def generate_image_embedding(self, gcs_uri):

        image = Image.load_from_file(gcs_uri)

        embedding = self.model.get_embeddings(
            image=image,
            dimension=512
        )

        return embedding.image_embedding
    

    def generate_text_embedding(self, text: str):

        """
        Optional.
        Generates text embedding for future text search.
        """

        embedding = self.model.get_embeddings(
            contextual_text=text,
            dimension=512
        )

        return embedding.text_embedding