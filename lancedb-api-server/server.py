import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import lancedb
import numpy as np
import uvicorn

app = FastAPI(title="LanceDB REST API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_options = {
    "region": os.getenv("LANCEDB_REGION", "us-east-1"),
    "endpoint": os.getenv("LANCEDB_ENDPOINT", "http://minio:9000"),
    "allow_http": os.getenv("LANCEDB_ALLOW_HTTP", "true"),
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", "admin"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", "minio12345"),
}

db = lancedb.connect(
    os.getenv("LANCEDB_URI", "s3://fluss-lakehouse/fluss"),
    storage_options=s3_options,
)

class CreateTableRequest(BaseModel):
    name: str
    data: List[Dict[str, Any]]

class InsertDataRequest(BaseModel):
    data: List[Dict[str, Any]]

class SearchRequest(BaseModel):
    vector: List[float]
    limit: int = 10

class UpdateRequest(BaseModel):
    where: str
    values: Dict[str, Any]

class DeleteRequest(BaseModel):
    where: str


@app.get("/")
async def root():
    return {"message": "LanceDB REST API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/tables")
async def list_tables():
    """List all tables in the database"""
    try:
        tables = db.table_names()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tables/{table_name}")
async def describe_table(table_name: str):
    """Get table schema and basic info"""
    try:
        table = db.open_table(table_name)
        return {
            "name": table_name,
            "schema": str(table.schema),
            "count": table.count_rows()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

@app.get("/tables/{table_name}/query")
async def query_table(
    table_name: str,
    query: str,
    limit: int = 100,
    offset: int = 0
):
    try:
        table = db.open_table(table_name)
        search_data = table.search().where(query).to_arrow().to_pylist()
        results = search_data[offset:offset+limit]
        return {
            "results": results,
            "count": len(results),
            "total": len(search_data)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
