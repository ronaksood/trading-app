import sqlite3 
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row # convert query data in the form of objects


cursor = connection.cursor()

# fetch data from the DB

cursor.execute("SELECT symbol,company FROM stock;")

rows = cursor.fetchall()

# now create an array symbol -> it will contain all symbols in a single array

symbols = [row['symbol'] for row in rows]

# it is same as 
# symbol = []
# for row in rows :
#     symbol.append(row['symbol'])

print(symbols)


# _____________________________________________________________________________________________



api_key = 'PKKHVNZCAVZQM5IJ4CDUIAKCXD'
secuirty_key = '9gtc86T5FcabfTiYhpFmMgVaEFbh1Z6dTRokkuQ88hZ6'

# now we have to call tradeapi.REST() 
# this is used to create alpaca api client
api = tradeapi.REST(api_key,secuirty_key,base_url = 'https://paper-api.alpaca.markets',api_version='v2')


assets = api.list_assets()

# here we have manually run the script to add new data to the database whenever we 
# have update in our data


for asset in assets:
    try: 
        # checking if the symbol is present in DB or not 
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols :
            print(f"Added a new stock : {asset.symbol}")
            cursor.execute("INSERT INTO stock(symbol,company) VALUES(?,?)" , (asset.symbol,asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

# therefore , using this tutorial we came to know that 
# we really need a cron job so that we dont have manually do this daily 


#______________________________________________________________________________________________


    
connection.commit()