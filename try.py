import sqlite3 , config 
import alpaca_trade_api as tradeapi
import datetime as currentdate
import alpha_vantage as tradeapi2
from alpha_vantage.timeseries import TimeSeries
import pandas as pd



connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

symbol = 'AAPL'

    # we will retrieve the minute bars of the whole day
ts = TimeSeries(key=config.VANTAGE_API_KEY,output_format='pandas')


  
minute_bars, meta_data = ts.get_intraday(symbol=symbol,interval='1min', )


# now the date is returning as an index to me 
# i have to make it a column
minute_bars = minute_bars.reset_index()
minute_bars.columns = ['date','open','high','low','close','volume']

cursor.execute("SELECT id FROM stock WHERE symbol = 'MSFT'")
stock_id = cursor.fetchone()['id']

# we need a stock id column for each row
minute_bars['stock_id'] = stock_id

# for minute in minute_bars:
#     print(minute)
#     cursor.execute("""
#         INSERT INTO intraday_prices
#             (stock_id,date,open,high,low,close,volume)
#             VALUES(? ,    ?   , ?  ,  ? , ? , ?   ,   ?  )
#         """,(stock_id,minute['dateTime'],minute['open'],minute['high'],minute['low'],minute['close'],minute['volume']))

minute_bars[['stock_id','date','open','high','low','close','volume']].to_sql("stock_price_minute" , connection , if_exists = 'append' , index = False)





    
