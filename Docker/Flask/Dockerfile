# Pythonのイメージを指定
FROM python:3.9-slim

# 作業ディレクトリを作成
RUN mkdir /code
WORKDIR /code

# requirements.txtをコンテナにコピーしてパッケージをインストール
COPY ../requirements.txt /code/
RUN pip install -U pip && \
    pip install -r requirements.txt

# ソースコードをコンテナにコピー
COPY ../app /code/

# 環境変数を設定
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Flaskアプリケーションを実行
CMD ["flask", "run", "--host=0.0.0.0"]
