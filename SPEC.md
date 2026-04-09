# WITHIN Rai Prototype — Build Spec

## Context & Purpose

Prem Patel is interviewing at WITHIN (within.co) for an AI Engineer role. He had an HM interview with Evan Vaughan (Head of Data) on Apr 8, 2026. Evan asked a live technical design question:

> "How would you add call transcripts and Slack channel data as knowledge sources into our internal chatbot Rai?"

Prem answered verbally. The goal of this prototype is to:
1. **Send to Evan and Patrick (recruiter) as a follow-up** — "I kept thinking about the problem, so I built it"
2. **Use as prep for Isaac's coding round** (next interview stage — technical)
3. **Use as prep for Mush's system design round** (stage after Isaac)

This should be a working demo with a shareable URL. It needs to be impressive but realistic — not over-engineered.

---

## What WITHIN Actually Builds

- Digital marketing agency (Nike, Hugo Boss, Ben & Jerry's, Casper as clients)
- Internal AI chatbot called **Rai** — used by ~200-500 employees (account managers)
- Rai currently queries a structured data warehouse (tabular ad performance data)
- They want to add: (1) call transcripts, (2) Slack channel data
- Team uses Claude Code heavily — Evan is a power user (skills, sub-agents, MCP tools)
- Key concern Evan raised: **no cross-client data contamination in generated outputs** (e.g. Casper's revenue figures must not appear in Nike's report)

---

## What This Prototype Must Demonstrate

1. **Transcript ingestion** — chunked, overlap, hybrid embeddings, metadata tagged by client + date
2. **Slack ingestion** — batched by time window, metadata tagged by client + channel
3. **Hybrid search** — dense (semantic) + sparse (keyword) — BGE-M3
4. **Client-level filtering** — query for "Casper" only returns Casper's data
5. **Date-aware retrieval** — more recent records ranked higher (Prem's post-interview addition)
6. **Source citations** in responses — which transcript/Slack message was used
7. **Live ingestion** — add a new transcript via endpoint, immediately queryable

These map 1:1 to what Prem said in the interview. The prototype is proof he can implement what he described.

---

## Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Vector DB | Qdrant Cloud (free tier) | Hosted, no Docker, hybrid search native, shareable |
| Embeddings | FlagEmbedding (BGE-M3) | Dense + sparse from same model — Prem's production stack |
| LLM | Anthropic Claude API (claude-sonnet-4-6) | Prem has API key |
| Backend | FastAPI | Prem's stack |
| Frontend | Streamlit | Fastest to ship a clean demo |
| Hosting | Render (free tier) | Simple FastAPI + Streamlit deploy, gives shareable URL |
| Language | Python 3.11+ | |

**Ask Prem before starting:**
- Does he have a Qdrant Cloud account? If not, create one at cloud.qdrant.io (free)
- Confirm Anthropic API key is available as env var `ANTHROPIC_API_KEY`
- Confirm preferred hosting: Render vs Railway vs local + ngrok for demo

---

## Synthetic Data

Three fake clients: **Casper**, **Nike**, **Hugo Boss**

### Call Transcripts (per client, 3-5 each)
Each transcript should include:
- Client-specific performance discussions (e.g. "Casper's Google Ads CTR dropped 12% last week")
- Campaign names, budget numbers, platform names (Facebook, Google, TikTok)
- Timestamps and meeting names
- Natural language — speaker labels optional but nice

Schema:
```json
{
  "transcript_id": "t_001",
  "client": "Casper",
  "meeting_name": "Weekly Performance Review",
  "date": "2026-04-07",
  "participants": ["Sarah (AM)", "Jake (Client)"],
  "text": "..."
}
```

### Slack Messages (per client channel, 10-20 messages each)
Each channel should include:
- Campaign launch announcements
- Performance observations
- Budget change requests
- Casual noise mixed in (to show filtering works)

Schema:
```json
{
  "message_id": "m_001",
  "client": "Casper",
  "channel": "casper-account",
  "user": "sarah_am",
  "timestamp": "2026-04-08T10:32:00",
  "text": "..."
}
```

---

## Project Structure

```
within-rai-prototype/
├── SPEC.md                        ← this file
├── README.md                      ← setup instructions
├── requirements.txt
├── .env.example
├── data/
│   └── synthetic/
│       ├── generate_data.py       ← generates transcripts.json + slack_messages.json
│       ├── transcripts.json       ← generated output
│       └── slack_messages.json    ← generated output
├── app/
│   ├── __init__.py
│   ├── main.py                    ← FastAPI app entry point
│   ├── config.py                  ← loads env vars
│   ├── models.py                  ← Pydantic request/response models
│   ├── embeddings.py              ← BGE-M3 dense + sparse via FlagEmbedding
│   ├── vector_store.py            ← Qdrant client, collection setup, upsert, search
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── transcript.py          ← chunk by paragraph + overlap, tag metadata, embed, upsert
│   │   └── slack.py               ← batch by time window, tag metadata, embed, upsert
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── rag.py                 ← hybrid search + metadata filter + Claude generation
│   └── routes/
│       ├── __init__.py
│       ├── ingest.py              ← POST /ingest/transcript, POST /ingest/slack
│       └── chat.py                ← POST /chat
└── frontend/
    └── app.py                     ← Streamlit UI
```

---

## API Endpoints

### POST /ingest/transcript
Simulates a transcript being ingested after a call ends.
```json
// Request
{
  "transcript_id": "t_001",
  "client": "Casper",
  "meeting_name": "Weekly Performance Review",
  "date": "2026-04-07",
  "text": "Full transcript text here..."
}

// Response
{
  "status": "ingested",
  "chunks": 4,
  "collection": "rai_knowledge_base"
}
```

### POST /ingest/slack
Simulates Slack channel data being ingested (batch of messages).
```json
// Request
{
  "client": "Casper",
  "channel": "casper-account",
  "messages": [
    {"user": "sarah_am", "timestamp": "2026-04-08T10:32:00", "text": "..."},
    ...
  ]
}

// Response
{
  "status": "ingested",
  "chunks": 3,
  "collection": "rai_knowledge_base"
}
```

### POST /chat
Query the RAG pipeline.
```json
// Request
{
  "query": "How did Casper's Facebook campaign perform last week?",
  "client": "Casper"  // optional — if provided, filters to this client only
}

// Response
{
  "answer": "Based on the Apr 7 review call...",
  "sources": [
    {"type": "transcript", "client": "Casper", "meeting": "Weekly Performance Review", "date": "2026-04-07"},
    {"type": "slack", "client": "Casper", "channel": "casper-account", "date": "2026-04-08"}
  ]
}
```

### GET /health
```json
{"status": "ok", "qdrant": "connected", "collections": ["rai_knowledge_base"]}
```

---

## Vector Store Design

### Collection: `rai_knowledge_base`

**Payload (metadata per chunk):**
```json
{
  "client": "Casper",
  "source_type": "transcript",  // or "slack"
  "date": "2026-04-07",
  "source_id": "t_001",
  "source_name": "Weekly Performance Review",  // meeting name or channel name
  "chunk_index": 2,
  "text": "The raw chunk text..."
}
```

**Filtering:**
- All queries filter by `client` field — this prevents cross-client contamination
- Date-weighted: use Qdrant's payload filter + re-rank by recency after retrieval

**Hybrid search:**
- Dense vector: BGE-M3 dense embeddings (semantic)
- Sparse vector: BGE-M3 sparse embeddings (keyword)
- Combine with RRF (Reciprocal Rank Fusion) or simple weighted sum

---

## Chunking Strategy

### Transcripts
- Split by paragraph (double newline)
- Chunk size: ~300-400 tokens
- Overlap: 50 tokens between chunks
- Prepend metadata to each chunk: `[Casper | Weekly Review | 2026-04-07]`

### Slack Messages
- Batch consecutive messages within a 30-minute window into one chunk
- If a single message is very long, split further
- Prepend: `[Casper | #casper-account | 2026-04-08]`

---

## RAG Generation (Claude Prompt)

```
You are Rai, an internal assistant for WITHIN's account managers.
Answer questions using only the provided context. Always cite your sources.
If the context doesn't contain enough information, say so honestly.
Never mix data from different clients.

Client context: {client}
Query: {query}

Context:
{retrieved_chunks}

Respond with:
1. A direct answer
2. Sources used (transcript name + date, or Slack channel + date)
```

---

## Streamlit UI

Simple two-panel layout:
- **Left sidebar:** Client selector (Casper / Nike / Hugo Boss / All), Data source filter (Transcripts / Slack / Both), "Seed sample data" button (runs ingestion on all synthetic data)
- **Main panel:** Chat interface with message history, source citations shown below each response

---

## Build Order

1. `data/synthetic/generate_data.py` — generate transcripts.json + slack_messages.json
2. `app/config.py` + `.env.example` — env var setup
3. `app/embeddings.py` — BGE-M3 dense + sparse
4. `app/vector_store.py` — Qdrant client, collection creation, upsert
5. `app/ingestion/transcript.py` + `slack.py`
6. `app/retrieval/rag.py` — hybrid search + Claude generation
7. `app/routes/ingest.py` + `chat.py`
8. `app/main.py` — wire everything together
9. `frontend/app.py` — Streamlit UI
10. Deploy: Render (FastAPI) + Qdrant Cloud
11. Smoke test with sample queries across clients
12. Verify no cross-client leakage

---

## Key Things to Get Right

- **Cross-client filtering must be enforced server-side**, not just prompt-level — Qdrant payload filter on every query
- **Hybrid search must use both vectors** — don't fall back to dense-only
- **Citations must be real** — pull from actual retrieved chunk metadata, not hallucinated
- **Date recency** — add a recency boost so Apr 8 beats Apr 1 for same relevance score
- **Ingestion is idempotent** — re-ingesting the same transcript_id should upsert, not duplicate

---

## After Building — Email to Send

Once hosted, Prem will send a short follow-up email to Patrick Ngo (patrick.ngo@within.co) to pass to Evan:

> Hi Patrick, I kept thinking about the technical question Evan asked around ingesting call transcripts and Slack data into Rai. I went ahead and built a small prototype this week — [link]. It's a working RAG pipeline with hybrid embeddings, client-level filtering, and live ingestion. Happy to walk Evan through it if useful. Looking forward to the next steps.

---

## Notes for the Claude Instance Building This

- Prem is an experienced ML/AI engineer — no need to over-explain concepts
- He wants clean, production-quality code — not tutorial-style comments
- He will run this locally first, then deploy — make sure local setup is straightforward
- Don't add features beyond what's in this spec — the scope is intentional
- If you hit a blocker (e.g. Qdrant Cloud credentials not set up), pause and ask Prem
- BGE-M3 via FlagEmbedding: `from FlagEmbedding import BGEM3FlagModel` — model name is `BAAI/bge-m3`
- For Qdrant hybrid search, use named vectors: one for dense (`dense`), one for sparse (`sparse`)
