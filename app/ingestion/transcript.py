from __future__ import annotations

from app.models import IngestTranscriptRequest
from app.vector_store import upsert_chunks

CHUNK_TARGET_WORDS = 300
OVERLAP_WORDS = 50


def _chunk_text(text: str) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: list[str] = []
    current_words: list[str] = []

    for para in paragraphs:
        para_words = para.split()
        current_words.extend(para_words)

        if len(current_words) >= CHUNK_TARGET_WORDS:
            chunks.append(" ".join(current_words))
            current_words = current_words[-OVERLAP_WORDS:]

    if current_words:
        if chunks:
            # Only add remainder as its own chunk if it has meaningful content
            if len(current_words) > OVERLAP_WORDS:
                chunks.append(" ".join(current_words))
            else:
                # Append to last chunk instead of creating a tiny fragment
                last = chunks[-1].split()
                last.extend(current_words[OVERLAP_WORDS:])
                chunks[-1] = " ".join(last)
        else:
            chunks.append(" ".join(current_words))

    return chunks


def ingest(req: IngestTranscriptRequest) -> int:
    raw_chunks = _chunk_text(req.text)
    prefix = f"[{req.client} | {req.meeting_name} | {req.date}]\n"

    payloads = []
    for i, chunk_text in enumerate(raw_chunks):
        payloads.append(
            {
                "client": req.client,
                "source_type": "transcript",
                "date": req.date,
                "source_id": req.transcript_id,
                "source_name": req.meeting_name,
                "chunk_index": i,
                "text": prefix + chunk_text,
            }
        )

    upsert_chunks(payloads)
    return len(payloads)
