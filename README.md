# SeLa

## 概要
- LangChain の勉強兼ねたパーソナルAIアプリケーション

## 環境準備
- tmp/conf.yaml に以下の情報を入れたファイルを作成してください
    - OPENAI_API_KEY: {OPENAIのAPIキー}
    - LANGCHAIN_API_KEY: {LangSmith のAPIキー}
    - LANGCHAIN_TRACING_V2: "true"
    - LANGCHAIN_ENDPOINT: https://api.smith.langchain.com
    - LANGCHAIN_PROJECT: sela

- tmp/aider.env に，Aiderの公式の設定ファイルをコピペしてください
    - https://github.com/Aider-AI/aider/blob/837b8a93e9561a274b09482d7d2a337ad0aa69b2/scripts/logo_svg.py
    - AIDER_OPENAI_API_KEY の設定だけ入れれば動きます

## 実行方法

### WebUI の起動
- Streamlit で起動します
```
streamlit run src/webui/main.py
```

### Aider の起動
- winpty経由で起動します
```
./aider_chat.sh
```
