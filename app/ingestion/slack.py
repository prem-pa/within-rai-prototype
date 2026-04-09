from __future__ import annotations

from datetime import datetime, timezone

from app.models import IngestSlackRequest, SlackMessage
from app.vector_store import upsert_chunks

WINDOW_MINUTES = 30


def _parse_ts(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def _batch_messages(messages: list[SlackMessage]) -> list[list[SlackMessage]]:
    sorted_msgs = sorted(messages, key=lambda m: _parse_ts(m.timestamp))
    if not sorted_msgs:
        return []

    batches: list[list[SlackMessage]] = []
    current_batch = [sorted_msgs[0]]
    window_start = _parse_ts(sorted_msgs[0].timestamp)

    for msg in sorted_msgs[1:]:
        ts = _parse_ts(msg.timestamp)
        if (ts - window_start).total_seconds() <= WINDOW_MINUTES * 60:
            current_batch.append(msg)
        else:
            batches.append(current_batch)
            current_batch = [msg]
            window_start = ts

    batches.append(current_batch)
    return batches


def ingest(req: IngestSlackRequest) -> int:
    batches = _batch_messages(req.messages)
    payloads = []

    for i, batch in enumerate(batches):
        batch_date = _parse_ts(batch[0].timestamp).date().isoformat()
        prefix = f"[{req.client} | #{req.channel} | {batch_date}]\n"
        lines = [f"{m.user}: {m.text}" for m in batch]
        chunk_text = prefix + "\n".join(lines)

        # Use channel + batch index as a stable source_id
        source_id = f"slack_{req.client}_{req.channel}"

        payloads.append(
            {
                "client": req.client,
                "source_type": "slack",
                "date": batch_date,
                "source_id": source_id,
                "source_name": req.channel,
                "chunk_index": i,
                "text": chunk_text,
            }
        )

    upsert_chunks(payloads)
    return len(payloads)
