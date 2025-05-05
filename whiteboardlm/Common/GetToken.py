from fastapi import HTTPException


def get_token(db, uid, token_type):
    doc_ref = db.collection(token_type).document(uid)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404)

    token_data = doc.to_dict()

    if token_type == "tokens_slack":
        slack_token = token_data.get('slackToken')
        app_token = token_data.get('appToken')
        return slack_token, app_token
    elif token_type == "tokens_discord":
        discord_token = token_data.get('discordToken')
        return discord_token
