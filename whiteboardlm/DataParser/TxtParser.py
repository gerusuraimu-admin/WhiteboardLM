import json

def txt2vec(file_content: bytes, max_length: int) -> str:
    try:
        text = file_content.decode('utf-8')

        if len(text) > max_length:
            text = text[:max_length]

        data = {
            "text": text
        }
        return json.dumps(data, indent=4, ensure_ascii=False)

    except UnicodeDecodeError:
        raise ValueError("ファイルのデコードに失敗しました。UTF-8形式ではない可能性があります。")
    except Exception as e:
        raise ValueError(f"予期しないエラーが発生しました: {str(e)}")
