from fastapi import APIRouter

from app.models import ChatRequest, ChatResponse
from app.retrieval import rag

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    return rag.retrieve_and_generate(req.query, req.client)
