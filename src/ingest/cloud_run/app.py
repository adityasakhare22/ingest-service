from fastapi import FastAPI
from src.ingest.cloud_run.service import IngestService

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
    
    
    
    return service.ingest_data()