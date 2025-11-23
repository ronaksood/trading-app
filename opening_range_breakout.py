import sqlite3 , config 
import alpaca_trade_api as tradeapi
import datetime as currentdate
import alpha_vantage as tradeapi2
from alpha_vantage.timeseries import TimeSeries

from main import index



connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# fetch the strategy id

cursor.execute("""
    SELECT id FROM strategy WHERE name = 'Opening_Range_Breakout'
""")

strategy_id = cursor.fetchone()['id']

print(strategy_id)

# fetch the stocks with that particular id

cursor.execute("""
    SELECT 
        stock.symbol , stock.name
    FROM stock JOIN stock_strategy
    ON stock.id = stock_strategy.stock_id
    WHERE stock_strategy.strategy_id = ?
""",(strategy_id,))

breakout_stocks = cursor.fetchall()

symbols = [stock['symbol'] for stock in breakout_stocks]

print(symbols)

# _________________________________________________________________________________________________

# now we have to fetch the minute bars of the whole day to perform strategies on the stock

# we are using alpha vantage api here because , alpacatradeapi is not providing minute frames

for symbol in symbols :
    # we will retrieve the minute bars of the whole day
    ts = TimeSeries(key=config.VANTAGE_API_KEY,output_format='pandas')

    # understand this -> this is very imp
    #  ts.get_intraday() function returns two things :-
    # 1. stock data that is being stored in the minute bars
    # 2. information about the request itself -> i.e. being stored in meta_data

    # output_size = "full" means return all the available intraday data
    # we can also use 'compact' here to get most recent data :-> it will just return 100 rows of data
  
    minute_bars, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')



    minute_bars = minute_bars.reset_index()
    minute_bars.columns = ['date','open','high','low','close','volume']

    # fetch stock id for every stock
    cursor.execute("""
        SELECT 
            id
        FROM stock 
        WHERE symbol = ?
    """,(symbol,))
    stock_id = cursor.fetchone()['id']


    minute_bars['stock_id'] = stock_id
    # now , we have to insert data for every symbol under opening_range_breakout
    minute_bars[['stock_id' , 'date' , 'open' , 'high' , 'low' , 'close' , 'volume']].to_sql('stock_price_minute', connection ,if_exists= 'append' ,index=False)

# column names by default are :-  1. open   2. high    3. low  4. close  5. volume
# we have to change these
    
