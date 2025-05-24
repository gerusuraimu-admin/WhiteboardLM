import requests


def respond(message: str, uid: str) -> str:
    url = 'https://whiteboardlm-gemma-112923488803.asia-northeast1.run.app/query'

    payload = {
        "message": message,
        "uid": uid
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        # return response.json().get("message", "応答が取得できませんでした。")
        return response.json()

    except requests.exceptions.RequestException as e:
        return f"RAGへのリクエストに失敗しました: {e}"
