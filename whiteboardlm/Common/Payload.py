from pydantic import BaseModel


class UIDPayload(BaseModel):
    uid: str


class EmbedRequest(BaseModel):
    path: str
    uid: str
