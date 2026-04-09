from __future__ import annotations

import uuid
from datetime import date, datetime

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    Fusion,
    MatchValue,
    NamedSparseVector,
    NamedVector,
    Prefetch,
    PointStruct,
    SparseIndexParams,
    SparseVectorParams,
    VectorParams,
    VectorsConfig,
)

from app.config import settings
from app.embeddings import embed

DENSE_DIM = 1024
DENSE_NAME = "dense"
SPARSE_NAME = "sparse"

_client: QdrantClient | None = None


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    return _client


def init_collection() -> None:
    client = get_client()
    existing = {c.name for c in client.get_collections().collections}
    if settings.collection_name in existing:
        return

    client.create_collection(
        collection_name=settings.collection_name,
        vectors_config={
            DENSE_NAME: VectorParams(size=DENSE_DIM, distance=Distance.COSINE),
        },
        sparse_vectors_config={
            SPARSE_NAME: SparseVectorParams(index=SparseIndexParams()),
        },
    )


def _chunk_point_id(source_id: str, chunk_index: int) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{source_id}:{chunk_index}"))


def upsert_chunks(chunks: list[dict]) -> None:
    if not chunks:
        return

    texts = [c["text"] for c in chunks]
    embeddings = embed(texts)
    client = get_client()

    points = []
    for chunk, emb in zip(chunks, embeddings):
        point_id = _chunk_point_id(chunk["source_id"], chunk["chunk_index"])
        points.append(
            PointStruct(
                id=point_id,
                vector={
                    DENSE_NAME: emb["dense"],
                    SPARSE_NAME: emb["sparse"],
                },
                payload=chunk,
            )
        )

    client.upsert(collection_name=settings.collection_name, points=points)


def _recency_factor(date_str: str, reference: date | None = None) -> float:
    """Return a small multiplier boost based on how recent the content is.

    More recent → higher boost. Max boost ~1.5x for today; decays to 1.0 at 90+ days.
    """
    if reference is None:
        reference = date.today()
    try:
        doc_date = date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return 1.0
    delta = (reference - doc_date).days
    decay = max(0.0, 1.0 - delta / 90.0)  # linear decay over 90 days
    return 1.0 + 0.5 * decay


def hybrid_search(
    query_text: str,
    client_filter: str | None = None,
    top_k: int = 6,
) -> list[dict]:
    client = get_client()
    query_emb = embed([query_text])[0]

    query_filter = None
    if client_filter:
        query_filter = Filter(
            must=[FieldCondition(key="client", match=MatchValue(value=client_filter))]
        )

    results = client.query_points(
        collection_name=settings.collection_name,
        prefetch=[
            Prefetch(
                query=NamedVector(name=DENSE_NAME, vector=query_emb["dense"]),
                using=DENSE_NAME,
                limit=top_k * 2,
                filter=query_filter,
            ),
            Prefetch(
                query=NamedSparseVector(
                    name=SPARSE_NAME,
                    vector=query_emb["sparse"],
                ),
                using=SPARSE_NAME,
                limit=top_k * 2,
                filter=query_filter,
            ),
        ],
        query=Fusion.RRF,
        limit=top_k,
        filter=query_filter,
        with_payload=True,
    )

    hits = []
    for point in results.points:
        payload = dict(point.payload)
        score = point.score
        # Apply recency boost using the date in payload
        doc_date = payload.get("date", "")
        score *= _recency_factor(doc_date)
        payload["_score"] = score
        hits.append(payload)

    # Re-sort after recency adjustment
    hits.sort(key=lambda x: x["_score"], reverse=True)
    return hits
