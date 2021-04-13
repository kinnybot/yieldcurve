from datetime import datetime

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import gif

gif.options.matplotlib['dpi'] = 200

@gif.frame
def plot(date, row):
  plt.plot(row.index, row.values, '-o')
  plt.title(date.date())
  plt.ylim((0, 7))

def fetch(tickers, start_date, end_date, file_name='curve.csv', csv=False):
  if csv:
    df = pd.read_csv(file_name, index_col=['DATE'], parse_dates=['DATE'])
  else:
    df = web.DataReader(tickers, 'fred', start_date, end_date)
    df.columns = df.columns.map(tickers)
    df.to_csv(file_name)
  return df

start_date = datetime(2000, 1, 1)
end_date = datetime.today()
tickers = { 'DGS1MO': '1M', 'DGS3MO': '3M', 'DGS6MO': '6M', 'DGS1': '1Y', 'DGS2': '2Y', 'DGS3': '3Y', 'DGS5': '5Y', 'DGS7': '7Y', 'DGS10': '10Y', 'DGS20': '20Y', 'DGS30': '30Y' }

df = fetch(tickers=tickers, start_date=start_date, end_date=end_date, csv=True)
df = df[~df.isna().any(axis=1)]
df = df.asfreq(freq='W', method='ffill')
frames = [plot(date, row) for date, row in df.iterrows()]
gif.save(frames, 'curve.gif', duration=120, unit='s', between='startend')