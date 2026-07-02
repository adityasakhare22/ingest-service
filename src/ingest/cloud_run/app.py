from fastapi import FastAPI
from src.ingest.cloud_run.service import IngestService
from fastapi import UploadFile, File
from src.ingest.cloud_run.service_search import SearchService




app = FastAPI(
    title="AI Data Ingestion POC",
    description="POC for ingesting data into BigQuery and Vector Search",
    version="1.0.0"
)


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