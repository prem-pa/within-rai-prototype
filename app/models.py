from pydantic import BaseModel


class SlackMessage(BaseModel):
    user: str
    timestamp: str
    text: str


class IngestTranscriptRequest(BaseModel):
    transcript_id: str
    client: str
    meeting_name: str
    date: str
    participants: list[str] = []
    text: str


class IngestSlackRequest(BaseModel):
    client: str
    channel: str
    messages: list[SlackMessage]


class IngestResponse(BaseModel):
    status: str
    chunks: int
    collection: str


class ChatRequest(BaseModel):
    query: str
    client: str | None = None


class Source(BaseModel):
    type: str          # "transcript" | "slack"
    client: str
    name: str          # meeting name or channel name
    date: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
