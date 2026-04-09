from fastapi import APIRouter

from app.config import settings
from app.ingestion import slack, transcript
from app.models import IngestResponse, IngestSlackRequest, IngestTranscriptRequest

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/transcript", response_model=IngestResponse)
async def ingest_transcript(req: IngestTranscriptRequest) -> IngestResponse:
    count = transcript.ingest(req)
    return IngestResponse(status="ingested", chunks=count, collection=settings.collection_name)


@router.post("/slack", response_model=IngestResponse)
async def ingest_slack(req: IngestSlackRequest) -> IngestResponse:
    count = slack.ingest(req)
    return IngestResponse(status="ingested", chunks=count, collection=settings.collection_name)
