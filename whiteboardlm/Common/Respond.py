import math
from itertools import chain
from google.cloud import storage, firestore
from vertexai.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

db = firestore.Client()


def respond(message: str, uid: str) -> str:
    task = 'RETRIEVAL_QUERY'
    model = TextEmbeddingModel.from_pretrained('textembedding-gecko')

    inputs = [TextEmbeddingInput(message, task)]
    vector = [embed.values for embed in model.get_embeddings(inputs)]
    flat_vectors = list(chain.from_iterable(vector))

    docs = db.collection('documents').where('uid', '==', uid).stream()
    best_doc = None
    best_score = -math.inf

    for doc in docs:
        data = doc.to_dict()
        if not data.get('embedding'):
            continue
        score = cosine_similarity(flat_vectors, data['embedding'])

        if score > best_score:
            best_score = score
            best_doc = data

    if best_doc:
        doc = read_file_from_gcs(best_doc.get('path'), 'whiteboardlm-v1.firebasestorage.app')
        if not doc.strip():
            doc = "参考文書なし"
        return llm_prompt(message, doc)
    else:
        return llm_prompt(message, '参考文書なし')


def cosine_similarity(v1, v2) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0


def read_file_from_gcs(path: str, bucket_name: str) -> str:
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)

        if not blob.exists():
            raise FileNotFoundError('GCSファイルが見つかりません')

        return blob.download_as_bytes().decode('utf-8', errors='ignore')
    except Exception as e:
        raise RuntimeError(f"GCSファイル読み込み失敗: {e}")


def llm_prompt(message: str, doc: str) -> str:
    model = GenerativeModel('gemini-pro')

    prompt = f"""
        以下の文書を参考にして、質問に答えてください。
        
        ---文書---
        {doc}
        
        ---質問---
        {message}
    """

    response = model.generate_content([Part.from_text(prompt)])
    return response.text.strip()
