# テスト用import
import random

test_phrases = [
    "こんにちは！何かお手伝いできることはありますか？",
    "承知しました。すぐに対応いたします。",
    "ご質問ありがとうございます。確認してご連絡します。",
    "了解しました。詳細を教えていただけますか？",
    "お待たせして申し訳ありません。"
]


def respond(message):
    return respond_test(message)


def respond_test(message):
    print('TEST MODE')
    print(message)

    phrase = random.choice(test_phrases)
    return phrase