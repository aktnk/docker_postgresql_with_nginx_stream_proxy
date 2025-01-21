from setting import db_session
from model import Sample
import pandas as pd

def add_data():
  electricity_df = pd.read_csv('./data/sample.csv')

  for index, _df in electricity_df.iterrows():
    row = Sample(code=_df['コード'], name=_df['名前'], bignum=_df['bignum'], flnum=_df['flnum'], date=_df['日付'], hour=_df['時間'])
    # データを追加する
    db_session.add(row)

  db_session.commit()

if __name__=="__main__":
  add_data()

  datas = db_session.query(Sample).all()
  for data in datas:
    print(f"{data.name}：{data.date} {data.hour}時 {data.bignum}")