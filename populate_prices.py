import sqlite3 , config
import alpaca_trade_api as tradeapi
from alpaca_trade_api import TimeFrame

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# fetching all the stocks from table stock

cursor.execute("SELECT id,symbol,name FROM stock")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]
symbols = [s for s in symbols if "/" not in s]

stock_dict = {}

# we are creating a dictionay lookup
# where our key is the symbol
# and the value is id of the stock {symbol : id}

for row in rows : 
    symbol = row['symbol'] # here , we accessed the symbol one by one
    # symbols.append(symbol) # adds symbol name at the end of symbols[]
    stock_dict[symbol] = row['id'] 

# connecting to api

api = tradeapi.REST(config.API_KEY , config.SECRECT_KEY,base_url = config.BASE_URL , api_version = config.VERSION)

# while fetching prices , we can just fetch prices of 200 stocks at a single time
# but we are not here to make thousands of api calls because we have 12000 stocks

#  we use the concept of chunking 
# in this , we will create a inner loop , in which we will loop to all 1-200 stocks 
# in second iteration we will loop through the 201-400 
# and so on

# TO UNDERSTAND THE CONCEPT , TRY RUNNING THIS

# chunk_size = 200
#          #    start    end          jump_size/increment
# for i in range(0 ,   len(symbols),chunk_size):
#     print(i) #start
#     print(i+chunk_size) #end
#     symbol_chunk = symbols[i:i+chunk_size] 
#     # in symbol_chunk -> we are assigning symbols from start to end for a particular chunk size
#     # it will store all symbols from 1-200 in 1st iteration and so on
#     print(symbol_chunk)

#_________________________________________________________________________________________

chunk_size = 200

for i in range(0 , len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    try :
        barset = api.get_bars(symbol_chunk,TimeFrame.Day,"2025-10-01","2025-10-30") 
        # in symbol_chunk -> we will get 200 symbols in a array , and we will get the bars of them
    except Exception as e:
        print(f"Skipping {symbol_chunk} due to error: {e}")


    # now we will iterate over these bars to store the info in stock_prices
    for bar in barset :
        print(f"Processing symbol : {bar.S}")
        stock_id = stock_dict[bar.S]
        cursor.execute("""
            INSERT INTO stock_prices
                (stock_id , date , open , high , low , close , volume)
            VALUES (?     ,   ?   ,  ?  ,  ?   ,   ? ,   ?   ,     ? )
        """, (stock_id, bar.t.date() , bar.o, bar.h,bar.l , bar.c, bar.v) )
      # here , stock_id is a foreign key refrence 
      # so how do we get the number associated with stock?
      # that's why we created stock_dict up there..                                                     
connection.commit()