# docker_postgresql_with_nginx_stream_proxy

## 構築手順

1. リポジトリを clone する
   ```
   $ git clone https://github.com/aktnk/docker_postgresql_with_nginx_stream_proxy.git postgresql_nginx`
   $ cd postgresql_nginx
   ```
1. PostgreSQL に関する設定情報を`.env`に記載する
   - 設定例
   ```.env
   POSTGRES_PASSWORD=password123
   POSTGRES_USER=user
   POSTGRES_DB=practice
   HOST=localhost
   ```
1. python の環境の作成

   1. python の仮想環境を作成
      ```
      $ pyenv local 3.10.3
      $ python -V
      Python 3.10.3
      $ python -m venv venv310
      $ source venv310/bin/activate
      (venv310) $
      ```
   1. モジュールをインストール
      ```
      (venv310) $ cd python
      (venv310) $ pip install -r requirements.txt
      ```

1. コンテナを起動する

   ```
   (venv310) $ cd ..
   (venv310) $ docker compose up -d
   (省略)
   (venv310) $ docker compose ps
   docker compose ps
   NAME                       IMAGE                     COMMAND                  SERVICE   CREATED          STATUS          PORTS
   nginx_postgresql-nginx-1   nginx:1.27.3-bookworm     "/docker-entrypoint.…"   nginx     38 seconds ago   Up 38 seconds   0.0.0.0:5555->5555/tcp, :::5555->5555/tcp, 0.0.0.0:8088->80/tcp, :::8088->80/tcp
   nginx_postgresql-pgsql-1   postgres:15.10-bookworm   "docker-entrypoint.s…"   pgsql     38 seconds ago   Up 38 seconds   5432/tcp
   ```

1. コンテナのログ確認
   - nginx コンテナ
   ```
   (venv310) $ docker compose logs nginx
   nginx-1  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
   nginx-1  | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
   nginx-1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
   nginx-1  | 10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf is not a file or does not exist
   nginx-1  | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
   nginx-1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
   nginx-1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
   nginx-1  | /docker-entrypoint.sh: Configuration complete; ready for start up
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: using the "epoll" event method
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: nginx/1.27.3
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: OS: Linux 5.15.167.4-microsoft-standard-WSL2
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: start worker processes
   nginx-1  | 2025/01/21 13:04:18 [notice] 1#1: start worker process 20
   (venv310) $
   ```
   - pgsql コンテナ
   ```
   (venv310) $ docker compose logs pgsql
   pgsql-1  | The files belonging to this database system will be owned by user "postgres".
   pgsql-1  | This user must also own the server process.
   pgsql-1  |
   pgsql-1  | The database cluster will be initialized with locale "en_US.utf8".
   pgsql-1  | The default database encoding has accordingly been set to "UTF8".
   pgsql-1  | The default text search configuration will be set to "english".
   pgsql-1  |
   pgsql-1  | Data page checksums are disabled.
   pgsql-1  |
   pgsql-1  | fixing permissions on existing directory /var/lib/postgresql/data ... ok
   pgsql-1  | creating subdirectories ... ok
   pgsql-1  | selecting dynamic shared memory implementation ... posix
   pgsql-1  | selecting default max_connections ... 100
   pgsql-1  | selecting default shared_buffers ... 128MB
   pgsql-1  | selecting default time zone ... Etc/UTC
   pgsql-1  | creating configuration files ... ok
   pgsql-1  | running bootstrap script ... ok
   pgsql-1  | performing post-bootstrap initialization ... ok
   pgsql-1  | syncing data to disk ... ok
   pgsql-1  |
   (省略)
   pgsql-1  |
   pgsql-1  | PostgreSQL init process complete; ready for start up.
   pgsql-1  |
   pgsql-1  | 2025-01-21 12:55:05.319 UTC [1] LOG:  starting PostgreSQL 15.10 (Debian 15.10-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
   pgsql-1  | 2025-01-21 12:55:05.320 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
   pgsql-1  | 2025-01-21 12:55:05.320 UTC [1] LOG:  listening on IPv6 address "::", port 5432
   pgsql-1  | 2025-01-21 12:55:05.323 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
   pgsql-1  | 2025-01-21 12:55:05.328 UTC [64] LOG:  database system was shut down at 2025-01-21 12:55:05 UTC
   pgsql-1  | 2025-01-21 12:55:05.332 UTC [1] LOG:  database system is ready to accept connections
   ```

## python から　 PostgreSQL にデータを登録する

### nginx stream proxy から PostgreSQL にデータを書き込んでみる

1. 準備
   - `.env`ファイルに記載した情報が表示されるはず
     ```
     (venv310) $ cd python
     (venv310) $ python postgresql_config.py
     user,password123,practice,localhost
     ```
1. PostgreSQL のデータベース practive にテーブルを作成する
   - SQLAlchemy を使いテーブルを定義している
     ```
     (venv310) aktnk@GBA5X1:~/projects/nginx_postgresql/python$ python model.py
     ```
1. サンプルデータ`data/sample.csv`を sample_table に登録する
   - 正常に登録できれば、下記のように登録したデータが表示される
     ```
     (venv310) aktnk@GBA5X1:~/projects/nginx_postgresql/python$ python sample.py
     name-1：2024-12-01 0時 0
     name-1：2024-12-01 1時 0
     name-1：2024-12-01 2時 0
     name-1：2024-12-01 3時 0
     name-1：2024-12-01 4時 0
     name-1：2024-12-01 5時 0
     (省略)
     ```

### qgsql コンテナからデータベース practice に sapmle_table が作成され、データ登録されていることを確認する

1. pqsql コンテナに入る
   ```
   (venv310) $ cd ..
   (venv310) $ docker compose exec -it pgsql bash
   ```
1. psql コマンドで practice データベースに user でログインする

   ```
    root@45995773014a:/# psql -U user -d practice
    psql (15.10 (Debian 15.10-1.pgdg120+1))
    Type "help" for help.

    practice=#
   ```

1. データベースをリストアップ

   ```
   practive=# \l
                                               List of databases
   Name    | Owner | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider | Access privileges
   -----------+-------+----------+------------+------------+------------+-----------------+-------------------
   postgres  | user  | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
   practice  | user  | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            |
   template0 | user  | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/user          +
           |       |          |            |            |            |                 | user=CTc/user
   template1 | user  | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/user          +
           |       |          |            |            |            |                 | user=CTc/user
   (4 rows)

   ```

1. テーブルを表示

   ```
    practice=# \d
                    List of relations
    Schema |        Name         |   Type   | Owner
    --------+---------------------+----------+-------
    public | sample_table        | table    | user
    public | sample_table_id_seq | sequence | user
    (2 rows)

    practice=# \d sample_table
                                    Table "public.sample_table"
    Column |         Type          | Collation | Nullable |                 Default
    --------+-----------------------+-----------+----------+------------------------------------------
    id     | integer               |           | not null | nextval('sample_table_id_seq'::regclass)
    code   | character varying(30) |           |          |
    name   | character varying(50) |           |          |
    bignum | bigint                |           |          |
    flnum  | double precision      |           |          |
    date   | date                  |           |          |
    hour   | integer               |           |          |
    Indexes:
        "sample_table_pkey" PRIMARY KEY, btree (id)
   ```

1. sample_table に登録したデータを表示

   ```
    practice=# select * from sample_table;
     id | code |  name  | bignum | flnum |    date    | hour
    ----+------+--------+--------+-------+------------+------
    1 | 11   | name-1 |      0 |     0 | 2024-12-01 |    0
    2 | 11   | name-1 |      0 |     0 | 2024-12-01 |    1
    3 | 11   | name-1 |      0 |     0 | 2024-12-01 |    2
    4 | 11   | name-1 |      0 |     0 | 2024-12-01 |    3
    5 | 11   | name-1 |      0 |     0 | 2024-12-01 |    4
    6 | 11   | name-1 |      0 |     0 | 2024-12-01 |    5
    7 | 11   | name-1 |      0 |     0 | 2024-12-01 |    6
    8 | 11   | name-1 |      0 |     0 | 2024-12-01 |    7
    9 | 11   | name-1 |      0 |     0 | 2024-12-01 |    8
    10 | 11   | name-1 |      0 |     0 | 2024-12-01 |    9
    11 | 11   | name-1 |      0 |     0 | 2024-12-01 |   10
    12 | 11   | name-1 |      0 |     0 | 2024-12-01 |   11
    13 | 11   | name-1 |      0 |     0 | 2024-12-01 |   12
    14 | 11   | name-1 |      0 |     0 | 2024-12-01 |   13
    15 | 11   | name-1 |      0 |     0 | 2024-12-01 |   14
    16 | 11   | name-1 |      0 |     0 | 2024-12-01 |   15
    17 | 11   | name-1 |      0 |     0 | 2024-12-01 |   16
    18 | 11   | name-1 |      0 |     0 | 2024-12-01 |   17
    19 | 11   | name-1 |      0 |     0 | 2024-12-01 |   18
    20 | 11   | name-1 |      0 |     0 | 2024-12-01 |   19
    21 | 11   | name-1 |      0 |     0 | 2024-12-01 |   20
    22 | 11   | name-1 |      0 |     0 | 2024-12-01 |   21
    23 | 11   | name-1 |      0 |     0 | 2024-12-01 |   22
    24 | 11   | name-1 |      0 |     0 | 2024-12-01 |   23
    25 | 11   | name-1 |      1 |     0 | 2024-12-02 |    0
    (省略)
   ```

1. コンテナから抜ける
   ```
    practice=# \q
    root@45995773014a:/# exit
    exit
    (venv310) $
   ```
