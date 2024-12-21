import os
import sys
import re
import requests
import uuid
import json

# APIキーを指定
KEY = os.getenv('AZURE_TRANSLATOR_API_KEY')

def translate(text):
    """テキストをAzure AI Translator APIにより翻訳する
    Args:
        text (str): 翻訳対象のテキスト
    Returns:
        str: APIからの戻り値（JSON）
    """
    # APIエンドポイントを指定
    endpoint = "https://api.cognitive.microsofttranslator.com/"

    # リクエストのパラメータを指定
    location = "JapanEast"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ['ja']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': KEY,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    # リクエストを送信して戻り値のJSONを取得
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    return request.json()


def insert_space_after_hash(text):
    """
    テキスト内の '\n#' の後に空白以外の文字が来る部分を見つけて、空白を挿入する関数
    Args:
        text (str): 処理対象のテキスト
    Returns:
        str: 空白が挿入されたテキスト
    """
    return re.sub(r'(\n#)(\S)', r'\1 \2', text)

def split_text_limitation(text, max_length=30000):
    """テキストを指定文字数くらいの改行文字で分割する
    Args:
        text (str): 分割対象のテキスト
        max_length (int): 分割する文字数
    Returns:
        list: 分割後のテキストのリスト
    """
    parts = []
    current_part = ''

    for line in text.splitlines(True):
        if (len(current_part) + len(line)) > max_length:
            parts.append(current_part)
            current_part = ''
        current_part = current_part + line

    if current_part:
        parts.append(current_part)

    return parts

# ファイルを読み込んで翻訳
fnDecorate = sys.argv[1]
sourcefile = 'sbj/'+fnDecorate+'.txt'
with open(sourcefile, 'r',encoding='UTF-8') as f:
    text = f.read()

text_parts = split_text_limitation(text)
responses = []
trans_sentence = ''

# 必要ならファイルを分割して処理する。エラー吐いたらそれ以上Azureにはアクセスしない。
for t in text_parts:
    res = translate(t)
    try:
        trans_sentence = trans_sentence + res[0]['translations'][0]['text']
        print('try_block finished')
    except ValueError as e:
        with open('sbj/'+fnDecorate+'.json', 'w') as f:
            json.dump(res, f, indent=2)
        print(e)
        sys.exit('ValueErrorが発生しています。入力が長すぎるかもしれません。translate関数のlength limitを変更することを検討してください。')
    finally:
        with open('sbj/'+fnDecorate+'.log','a') as f:
            f.write(json.dumps(res, ensure_ascii=False)+'\n')

        print('output_log finished')

# 翻訳結果をファイルに保存
file_name = 'sbj/'+fnDecorate+'_translated.txt'
with open(file_name, 'w', encoding='Shift-JIS') as f:
    fixed_text = insert_space_after_hash(trans_sentence)
    f.write(fixed_text)

print('output_txt finished')