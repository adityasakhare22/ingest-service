from fastapi import FastAPI
from src.ingest.cloud_run.service import IngestService
from fastapi import UploadFile, File
from src.ingest.cloud_run.service_search import SearchService
from pydantic import BaseModel



app = FastAPI(
    title="AI Data Ingestion POC",
    description="POC for ingesting data into BigQuery and Vector Search",
    version="1.0.0"
)

class TextSearchRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {
        "status": "UP"
    }



@app.post("/ingest")
def ingest():
    service = IngestService()
    return service.ingest_data()
    
    
    #return IngestService.ingest_data()

@app.post("/search/image")
async def search_image(file: UploadFile = File(...)):

    service = SearchService()

    return await service.search_image(file)    

@app.post("/search/text")
async def search_text(request: TextSearchRequest):

    service = SearchService()

    return service.search_text(request.text)