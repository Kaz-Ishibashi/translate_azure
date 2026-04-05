# translate_azure

Azure AI Translator API を使って、英語の長文テキストを日本語へ翻訳するツールです。  
Python で翻訳処理を行い、PowerShell で実行とクリップボードへのコピーを担当します。  
英語論文や技術記事の翻訳時に発生しがちな、翻訳サービスへの分割コピペ作業を減らすことを目的としています。

## Features

- Azure AI Translator API を利用した英日翻訳
- 長文テキストをファイル単位で処理
- 翻訳結果をテキストファイルとして保存
- PowerShell からワンコマンドで実行可能
- 翻訳後のテキストをクリップボードへ自動コピー
- Markdown 見出しの崩れを簡易補正

## Environment

動作確認環境:

- Windows 11 23H2
- Python 3.12.2
- PowerShell 7.4.6
- Azure for Students

## Directory Structure

```text
<project_root>
├─ azure.py
├─ azure_translate.ps1
└─ sbj/
   ├─ sample.txt
   └─ sample_translated.txt
```

- `azure.py`  
  翻訳対象ファイルを読み込み、Azure AI Translator API を呼び出して翻訳結果を保存します。

- `azure_translate.ps1`  
  Python スクリプトを起動し、生成された翻訳結果をクリップボードにコピーします。

- `sbj/`  
  入力ファイルと出力ファイルを配置するディレクトリです。

## Setup

### 1. Azure AI Translator API の準備

Azure ポータルで Translator リソースを作成し、API キーを取得してください。  
記事では、リージョンに `Japan East`、価格レベルに `Free (F0)` を設定する流れが紹介されています。

### 2. 環境変数を設定

API キーを環境変数に設定してください。

```powershell
AZURE_TRANSLATOR_API_KEY
```

### 3. 依存ライブラリをインストール

`requests` を使用します。

```bash
pip install requests
```

## Usage

### 1. 翻訳したい英語テキストを用意

`sbj/` ディレクトリ内に、UTF-8 でテキストファイルを保存します。  
たとえば `sample.txt` を翻訳したい場合は、以下のような構成にします。

```text
sbj/sample.txt
```

### 2. PowerShell から実行

```powershell
./azure_translate.ps1 sample
```

### 3. 実行結果

- `sbj/sample_translated.txt` が生成されます
- 訳文がクリップボードへ自動コピーされます

## Implementation

### Python (`azure.py`)

Python 側では以下を担当します。

- テキストファイルの読み込み
- Azure AI Translator API の呼び出し
- レスポンス JSON から翻訳結果を取得
- Markdown 見出しの崩れの補正
- 翻訳結果の保存

記事内の実装では、入力ファイルを `UTF-8`、出力ファイルを `Shift-JIS` で扱っています。  
また、改行直後の `#` に空白が入っていない場合を正規表現で補正する処理が含まれています。

### PowerShell (`azure_translate.ps1`)

PowerShell 側では以下を担当します。

- コマンドライン引数の受け取り
- Python スクリプトの実行
- 翻訳済みテキストの読み込み
- クリップボードへのコピー

## Example

```powershell
~/translate> ./azure_translate.ps1 sample
translation completed.
```

この時点で、翻訳結果はクリップボードにコピーされています。

## Notes

- 現在の構成では、`azure.py`、`azure_translate.ps1`、`sbj/` を想定したディレクトリ配置になっています。
- パスの記述が固定寄りのため、配置を変更する場合はコードの修正が必要です。
- 翻訳方向は記事内実装では `en -> ja` に設定されています。
- リージョンはコード内で `JapanEast` を使用しています。

## Motivation

英語論文や長文記事の翻訳では、多くの翻訳サービスに文字数制限があり、何度もコピペを繰り返す必要があります。  
このツールは、その手間をできるだけ減らし、論文調査や技術記事の読解を効率化するために作成しました。

## Future Work

- 翻訳 API の切り替え対応
- ディレクトリ構成やパス指定の柔軟化
- エラーハンドリングの強化
- 複数ファイルの一括翻訳

## Reference

- Qiita: 【超長文対応】AzureとPythonで長文を一瞬で翻訳する方法【面倒なコピペ排除】【200万文字まで無料】
