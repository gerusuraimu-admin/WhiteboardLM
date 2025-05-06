from typing import Optional
from dataclasses import dataclass
from fastapi import HTTPException


@dataclass
class FileMetadata:
    uid: str
    filename: str
    path: str
    size: int
    uploaded_at: Optional[str] = None
    processed: bool = False
    embedding_id: Optional[str] = None
    id: Optional[str] = None

    def __str__(self) -> str:
        return ''.join(f'{k.ljust(11)} : {v}' for k, v in vars(self).items())


def get_file_metadata(db, data):
    try:
        filename = data.path.split('/')[-1]
        doc_id = f"{data.uid}_{filename}"

        doc_ref = db.collection('documents').document(doc_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="ドキュメントが存在しません")

        doc_data = doc.to_dict()
        return FileMetadata(
            uid=doc_data.get("uid"),
            filename=doc_data.get("filename"),
            path=doc_data.get("path"),
            size=doc_data.get("size"),
            uploaded_at=str(doc_data.get("uploaded_at")) if doc_data.get("uploaded_at") else None,
            processed=doc_data.get("processed", False),
            embedding_id=doc_data.get("embedding_id"),
            id=doc.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
