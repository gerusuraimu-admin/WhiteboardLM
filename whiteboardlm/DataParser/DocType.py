from enum import Enum
from whiteboardlm import txt2vec


class DocType(Enum):
    txt: str = ('text/plain', txt2vec)

    def __init__(self, mime, handler):
        self.mime = mime
        self.handler = handler
