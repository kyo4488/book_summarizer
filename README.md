# book summarizer
このリポジトリは、指定された本の内容を要約します。

---

## 環境

- Poetry

---

## 実行手順
### 1. リポジトリのクローン

```
git clone <リポジトリURL>
cd book_summarizer
```

### 2.Poetryのインストール
Poetry環境がなければ、以下のコードなどを実行してPoetryをインストールしてください。

```
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. 依存パッケージのインストール

```
poetry install
```

### 4. .envファイルの作成
.envファイルを作成し、以下のように記述してください。
```
OPENAI_API_KEY=<your_openai_api_key>
```

### 5. データの用意
`data`ディレクトリを作成し、要約したい本のテキストファイルを`book.txt`という名前で保存してください。

### 6. 実行
以下のコードで要約が実行されます。
```
make run
```