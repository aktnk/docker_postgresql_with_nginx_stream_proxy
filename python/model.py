from sqlalchemy import Column, BigInteger, Integer, Float, String, Date
from setting import engine, Base

# テーブルを定義する
# Baseを継承
class Sample(Base):
  # テーブル名
  __tablename__ = 'sample_table'
  # カラムの定義
  id = Column(Integer, primary_key=True, autoincrement=True)
  code = Column(String(30), unique=False)
  name = Column(String(50), unique=False)
  bignum = Column(BigInteger, unique=False)
  flnum = Column(Float, unique=False)
  date = Column(Date, unique=False)
  hour = Column(Integer, unique=False)

  
  def __init__(self, code=None, name=None, bignum=None, flnum=None, date=None, hour=None):
    self.code = code
    self.name = name
    self.bignum= bignum
    self.flnum = flnum
    self.date = date
    self.hour = hour

if __name__=="__main__":
    Base.metadata.create_all(bind=engine)
