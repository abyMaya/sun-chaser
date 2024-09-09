# MySQL8系のイメージを指定
From mysql:8.0

# MySQLのローカルの設定ファイルをコンテナにコピー
COPY Docker/MySQL/my.cnf /etc/mysql/conf.d/mycnf
# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY Docker/MySQL/init.sql /docker-entrypoint-initdb.d
