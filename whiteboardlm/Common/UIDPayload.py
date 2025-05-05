from pydantic import BaseModel


class UIDPayload(BaseModel):
    uid: str
