import json
import os
from pathlib import Path

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

CLIENTS = ["Casper", "Nike", "Hugo Boss"]
DATA_DIR = Path(__file__).parent.parent / "data" / "synthetic"


def seed_data():
    transcripts_path = DATA_DIR / "transcripts.json"
    slack_path = DATA_DIR / "slack_messages.json"

    if not transcripts_path.exists() or not slack_path.exists():
        st.error("Synthetic data files not found. Run: python data/synthetic/generate_data.py")
        return

    with open(transcripts_path) as f:
        transcripts = json.load(f)
    with open(slack_path) as f:
        slack_messages = json.load(f)

    progress = st.progress(0, text="Seeding data...")
    total = len(CLIENTS) * 2  # transcripts + slack per client
    step = 0

    for client in CLIENTS:
        client_transcripts = [t for t in transcripts if t["client"] == client]
        for t in client_transcripts:
            httpx.post(f"{API_URL}/ingest/transcript", json=t, timeout=120)
        step += 1
        progress.progress(step / total, text=f"Ingested {client} transcripts...")

        client_msgs = [m for m in slack_messages if m["client"] == client]
        channel = client_msgs[0]["channel"] if client_msgs else f"{client.lower().replace(' ', '')}-account"
        payload = {
            "client": client,
            "channel": channel,
            "messages": [{"user": m["user"], "timestamp": m["timestamp"], "text": m["text"]} for m in client_msgs],
        }
        httpx.post(f"{API_URL}/ingest/slack", json=payload, timeout=120)
        step += 1
        progress.progress(step / total, text=f"Ingested {client} Slack messages...")

    progress.progress(1.0, text="Done!")
    st.success(f"Seeded {len(transcripts)} transcripts and {len(slack_messages)} Slack messages.")


# ── Layout ──────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Rai — WITHIN Knowledge Assistant", page_icon="🤖", layout="wide")
st.title("Rai — WITHIN Knowledge Assistant")

with st.sidebar:
    st.header("Settings")
    client_choice = st.selectbox("Client", ["All"] + CLIENTS)
    selected_client = None if client_choice == "All" else client_choice

    st.divider()
    st.subheader("Data")
    if st.button("Seed sample data", use_container_width=True):
        seed_data()

    st.divider()
    try:
        health = httpx.get(f"{API_URL}/health", timeout=5).json()
        qdrant_status = health.get("qdrant", "unknown")
        color = "green" if qdrant_status == "connected" else "orange"
        st.markdown(f"**API:** :green[connected]")
        st.markdown(f"**Qdrant:** :{color}[{qdrant_status}]")
    except Exception:
        st.markdown("**API:** :red[unreachable]")

# ── Chat ─────────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if selected_client:
    st.caption(f"Filtering to: **{selected_client}** — cross-client data is excluded")
else:
    st.caption("Querying across all clients")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources"):
                for src in msg["sources"]:
                    icon = "📞" if src["type"] == "transcript" else "💬"
                    st.markdown(f"{icon} **{src['type'].title()}** — {src['name']} — {src['client']} — {src['date']}")

if prompt := st.chat_input("Ask about campaign performance, budgets, or strategy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                payload = {"query": prompt}
                if selected_client:
                    payload["client"] = selected_client
                resp = httpx.post(f"{API_URL}/chat", json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                answer = data["answer"]
                sources = data.get("sources", [])
            except Exception as e:
                answer = f"Error contacting API: {e}"
                sources = []

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for src in sources:
                    icon = "📞" if src["type"] == "transcript" else "💬"
                    st.markdown(f"{icon} **{src['type'].title()}** — {src['name']} — {src['client']} — {src['date']}")

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
