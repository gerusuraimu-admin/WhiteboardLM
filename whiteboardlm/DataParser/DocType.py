from enum import Enum
from whiteboardlm.DataParser.TxtParser import txt2vec


class DocType(Enum):
    txt: str = ('text/plain', txt2vec)

    def __init__(self, mime, handler):
        self.mime = mime
        self.handler = handler
