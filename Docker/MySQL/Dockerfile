# MySQL8系のイメージを指定
FROM mysql:8.0

# ロケールの設定を追加
ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8

# MySQLのローカルの設定ファイルをコンテナにコピー
COPY Docker/MySQL/my.cnf /etc/mysql/conf.d/my.cnf
# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY Docker/MySQL/init.sql /docker-entrypoint-initdb.d

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8 \
    && update-locale LANG=ja_JP.UTF-8
