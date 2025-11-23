import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame

api = tradeapi.REST(config.API_KEY,config.SECRECT_KEY,base_url = config.BASE_URL,api_version=config.VERSION)


# go to alpaca trade api python for knowing these functions

barsets = api.get_bars(['AAPL' , 'MSFT'] , TimeFrame.Day,"2025-10-22","2025-10-22")

print(barsets)


# this get_bars() function is used to fetch stock prices 
#  it will return a bar object in which we will have
#  close price , open price , high price , volume etc.

# ouput like -> 
# [Bar({   'S': 'AAPL',
#     'c': 269.7,
#     'h': 271.41,
#     'l': 267.11,
#     'n': 687379,
#     'o': 269.275,
#     't': '2025-10-29T04:00:00Z',
#     'v': 51087269,
#     'vw': 269.541775}), Bar({   'S': 'MSFT',
#     'c': 541.55,
#     'h': 546.27,
#     'l': 536.7287,
#     'n': 876838,
#     'o': 544.94,
#     't': '2025-10-29T04:00:00Z',
#     'v': 36023174,
#     'vw': 539.842709})]

# when we our accessing intraday or every minute detail
# it is possible that we can see some gaps in minute , beacuse we are using a free api
# it gives details about some certain exchanges only

#______________________________________________________________________________________________


# loop over the bar in barset


# for bar in barsets:
#     print(f"Formatting symbol {bar.S}") 
    
#     print(bar.t , bar.o, bar.h , bar.l , bar.c , bar.v)