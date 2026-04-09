from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, ingest
from app.vector_store import get_client, init_collection
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_collection()
    yield


app = FastAPI(title="Rai Knowledge API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(chat.router)


@app.get("/health")
async def health():
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]
    qdrant_status = "connected" if settings.collection_name in collections else "collection_missing"
    return {"status": "ok", "qdrant": qdrant_status, "collections": collections}
