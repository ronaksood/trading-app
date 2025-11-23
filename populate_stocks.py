import sqlite3 ,config
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row # convert query data in the form of objects


cursor = connection.cursor()

# here we cannot add data one by one like this -> 
# cursor.execute("""
#     INSERT INTO stock(symbol,company) VALUES('AAPL', 'Apple Inc.')
# """
# )
# because in trading application , we need thousands and thousands of stocks

# _____________________________________________________________________________________________

# lets see how to fetch results from database using python
# the thing here is what we dont want to access the data from our rows array
# using indexes -> it is not a good approach


# we want to access data in the form of objects : to do this
# we will use connection.row_factory = sqlite3.Row

# why -> whenever we will query our data
# it will return us data in the form of objects


# cursor.execute("SELECT symbol,company FROM stock;")
# rows = cursor.fetchall()

# for row in rows :
#     print(row['symbol'])

#______________________________________________________________________________________________

# how to create a TRADABLE STOCK UNIVERSE
#  we can use ftp files of nasdaq but it provides raw information
# these ftp files needs to be downloaded individually 
#  and the data inside these ftp files needed to be cleaned up

# _____________________________________________________________________________________________


# so we are going to use a api for it
# pip install alpaca-trade-api
# it provides list of tradable assets , AND market data

# _____________________________________________________________________________________________



# api_key = 'PKKHVNZCAVZQM5IJ4CDUIAKCXD'
# secuirty_key = '9gtc86T5FcabfTiYhpFmMgVaEFbh1Z6dTRokkuQ88hZ6'

# now we have to call tradeapi.REST() 
# this is used to create alpaca api client
api = tradeapi.REST(config.API_KEY,config.SECRECT_KEY,base_url = config.BASE_URL,api_version=config.VERSION)


assets = api.list_assets()




# here , list assests function is returning all the assets
# assets we are getting are in the form of objects
# we can access the attributes of these assets


#_________________________________________________________________________

# for printing the assets 

# for asset in assets:
#     print(asset)


# for accessing names of the assets


# for asset in assets:
#     print(asset.name)

#___________________________________________________________________________

# now , i have to insert data inside the database 
# lets add data in table

# dont forget to handle the exceptions
# like here , we can face the exception that more than one assest can have same symbol
# and we have unique constraint on symbol in our table




for asset in assets:
    try: 
        # we only need to insert active companies 
        # and we only need tradable stocks
        if asset.status == 'active' and asset.tradable :
            cursor.execute("INSERT INTO stock(symbol,name,exchange) VALUES(?,?,?)" , (asset.symbol,asset.name,asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

#______________________________________________________________________________________________


    
connection.commit()