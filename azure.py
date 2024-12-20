import os
import sys
import re
import requests
import uuid
import json

# APIキーを指定
KEY = os.getenv('AZURE_TRANSLATOR_API_KEY')

def translate(text, fn = 'default'):
    """テキストをAzure AI Translator APIにより翻訳する
    Args:
        text (str): 翻訳対象のテキスト
        fn (str): 出力ファイル名から拡張子を除いたもの
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
    response = request.json()

    # 翻訳結果をファイルに保存
    file_name = 'sbj/'+fn+'_translated.txt'
    with open(file_name, 'w', encoding='Shift-JIS') as f:
        try:
            fixed_text = insert_space_after_hash(response[0]['translations'][0]['text'])
            f.write(fixed_text)
        except:
            json.dump(response, f, indent=2)

def insert_space_after_hash(text):
    # 正規表現で '\n#' の後に空白以外の文字が来る部分を見つけて、空白を挿入
    return re.sub(r'(\n#)(\S)', r'\1 \2', text)

def split_text_limitation(text, max_length=30000):
    """テキストを指定文字数で分割する
    Args:
        text (str): 分割対象のテキスト
        max_length (int): 分割する文字数
    Returns:
        list: 分割後のテキストのリスト
    """
    parts = []
    current_part = ''
    current_length = 0

    for line in text.splitlines(True):



# ファイルを読み込んで翻訳
fnDecorate = sys.argv[1]
sourcefile = 'sbj/'+fnDecorate+'.txt'
with open(sourcefile, 'r',encoding='UTF-8') as f:
    text = f.read()

print(len(text))
# translate(text, fnDecorate)