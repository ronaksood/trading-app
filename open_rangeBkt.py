import sqlite3 , config 
import alpaca_trade_api as tradeapi
from datetime import datetime
import alpha_vantage as tradeapi2
from alpha_vantage.timeseries import TimeSeries

from main import index



connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

api = tradeapi.REST(config.API_KEY,config.SECRECT_KEY,base_url = config.BASE_URL,api_version=config.VERSION)


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

start_minute_bar = '2025-11-18 09:30:00'
end_minute_bar = '2025-11-18 09:45:00'


# for symbol in symbols :
 
#     # fetch stock id for every stock
#     cursor.execute("""
#         SELECT 
#             id
#         FROM stock 
#         WHERE symbol = ?
#     """,(symbol,))
#     stock_id = cursor.fetchone()['id']


#     # now we have to fetch data of 15 min range of current date
#     # i only need min low , max high of that time to find range
#     cursor.execute("""
#         SELECT stock_id , MIN(low) AS low, MAX(high) AS high
#         FROM stock_price_minute
#         WHERE date >= ? AND date <= ? AND stock_id = ?
#     """ , (start_minute_bar , end_minute_bar , stock_id))

#     opening_range_mask = cursor.fetchone()

#     # low of the 15 min
#     opening_range_low = round(opening_range_mask['low'],2)
#     # high of the 15 min
#     opening_range_high = round(opening_range_mask['high'],2)

#     # range of the 15 min
#     opening_range = round(opening_range_high - opening_range_low,2)

#     print(opening_range_low)
#     print(opening_range_high)
#     print(opening_range)


#     # after every minute 
#     # we will check the closing prices 
#     # if closing price is greater then the opening_range_high
#     # then we will enter the trade
#     # put a target of close + opening_range
#     # put a stopLoss of close - opening_range

#     # check in the after minute bars
#     cursor.execute("""
#         SELECT * 
#         FROM stock_price_minute 
#         WHERE date > ? AND close > ? AND stock_id = ?
#     """ , (end_minute_bar,opening_range_high,stock_id))
#     after_minute_bars = cursor.fetchall()

#     # if after_min is not empty
#     if after_minute_bars:
#         for minute in after_minute_bars:
#             print(minute['close'])
#             limit_price = round(minute['close'],2)
#             api.submit_order(
#                 symbol=symbol,
#                 side='buy',
#                 type='limit',
#                 limit_price= limit_price,
#                 qty='2',
#                 time_in_force='day',
#                 order_class='bracket',
#                 take_profit=dict(
#                     limit_price=round(limit_price + opening_range,2),
#                 ),
#                 stop_loss=dict(
#                     stop_price=round(limit_price - opening_range,2),
#                 )
#             )
#             print(f"Placed Order : {symbol} , Limit Price :{limit_price} , target : {limit_price+opening_range}")


api.submit_order(
                symbol='AAMI',
                side='sell',
                type='market',
                qty='10',
                time_in_force='day'
                
            )

    
