from google.cloud import storage
from fastapi import HTTPException
import mimetypes
from whiteboardlm import DocType


def read_file_from_gcs(path: str, bucket_name: str) -> bytes:
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(path)

        if not blob.exists():
            raise HTTPException(status_code=404, detail=f"GCSファイルが見つかりません: {path}")

        return blob.download_as_bytes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GCSファイル読み込み失敗: {e}")


def detect_file_type(path: str) -> DocType:
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        raise HTTPException(status_code=400, detail="ファイルタイプを特定できません")
    return DocType(mime_type)
