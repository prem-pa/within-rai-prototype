from __future__ import annotations

import anthropic

from app.config import settings
from app.models import ChatResponse, Source
from app.vector_store import hybrid_search

_client: anthropic.Anthropic | None = None

SYSTEM_PROMPT = """You are Rai, an internal assistant for WITHIN's account managers.
Answer questions using only the provided context. Always cite your sources.
If the context doesn't contain enough information, say so honestly.
Never mix data from different clients — stay strictly within the client context provided."""


def _build_context_block(hits: list[dict]) -> str:
    blocks = []
    for i, hit in enumerate(hits, 1):
        source_type = hit.get("source_type", "unknown")
        name = hit.get("source_name", "")
        date = hit.get("date", "")
        label = f"[Source {i}: {source_type} — {name} — {date}]"
        blocks.append(f"{label}\n{hit['text']}")
    return "\n\n---\n\n".join(blocks)


def _dedupe_sources(hits: list[dict]) -> list[Source]:
    seen: set[tuple] = set()
    sources: list[Source] = []
    for hit in hits:
        key = (hit.get("source_type"), hit.get("source_id"))
        if key not in seen:
            seen.add(key)
            sources.append(
                Source(
                    type=hit.get("source_type", "unknown"),
                    client=hit.get("client", ""),
                    name=hit.get("source_name", ""),
                    date=hit.get("date", ""),
                )
            )
    return sources


def retrieve_and_generate(query: str, client: str | None) -> ChatResponse:
    hits = hybrid_search(query, client_filter=client, top_k=6)

    if not hits:
        return ChatResponse(
            answer="I don't have any relevant information in the knowledge base for that query.",
            sources=[],
        )

    context = _build_context_block(hits)
    client_context = client or "All clients"

    user_message = f"""Client context: {client_context}
Query: {query}

Context:
{context}

Respond with:
1. A direct answer based only on the context above
2. Sources used (transcript meeting name + date, or Slack channel + date)"""

    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    answer = message.content[0].text
    sources = _dedupe_sources(hits)

    return ChatResponse(answer=answer, sources=sources)
