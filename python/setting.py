from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base

import pandas as pd

import postgresql_config

user = postgresql_config.DB_USER
password = postgresql_config.DB_PASSWORD
host = postgresql_config.DB_HOST
db_name = postgresql_config.DB_DATABASE

# engineの設定
#engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}')
engine = create_engine(f'postgresql://{user}:{password}@{host}:5555/{db_name}')


# セッションの作成
db_session = scoped_session(
  sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
  )
)

# テーブルを作成する
Base = declarative_base()
Base.query  = db_session.query_property()