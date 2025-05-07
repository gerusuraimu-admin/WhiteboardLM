from enum import Enum
from whiteboardlm.DataParser.TxtParser import txt2vec


class DocType(Enum):
    txt = ('text/plain', txt2vec)

    def __init__(self, mime, handler):
        self.mime = mime
        self.handler = handler

    @classmethod
    def from_mime(cls, mime_type):
        for doc_type in cls:
            if doc_type.mime == mime_type:
                return doc_type
        raise ValueError(f"'{mime_type}' is not a valid DocType")
