from dotenv import load_dotenv
load_dotenv()
from urllib import request
from fastapi import FastAPI, Form , Request
import sqlite3 , config


from numpy import empty


from fastapi.responses import RedirectResponse

import finnhub
from datetime import date , timedelta , timezone , datetime

from zoneinfo import ZoneInfo


#  import jinja 2 template to return html template for the view
# go to fastApi website -> templates
from fastapi.templating import Jinja2Templates



app = FastAPI() # creating an instance of fastAPI
templates = Jinja2Templates(directory="templates") # creating an instaance of template
#  we will create a folder for templates where we will write our view logic


@app.get("/") # it acts as a router  : ex -> localhost/
def index(request:Request): # we'll get the result in '/' route whatever this function will return
    return templates.TemplateResponse("main.html",{"request":request}) # by default this returns a json object
# fast api is built for backend apis by default

# to return a template -> we have to pass a request object to the function
# request object contains -> ip address of user , user info etc
@app.get("/stock")
def index(request : Request):
    # there is alot of info packed in request object 
    # to use the templates we have to use this request object

    # using request object , we can also access the query string of the url
    # here request.query_params is used to get the query string variables
    stock_filter = request.query_params.get("filter",False)

    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row


    cursor = connection.cursor()

    if stock_filter == "new_intraday_highs" :
        cursor.execute("""
            SELECT * FROM (
                SELECT 
	                stock_prices.stock_id,
	                stock.symbol,
	                stock.name,
	                MAX(stock_prices.high) as price,
	                stock_prices.date
                FROM stock JOIN stock_prices
                ON stock.id = stock_prices.stock_id
                GROUP BY stock_id
            ) WHERE date = '2025-10-30'
            ORDER BY symbol ASC;
        """)
        rows = cursor.fetchall()

        return templates.TemplateResponse("stock_filter.html",{"request" : request , "stocks" : rows})
    elif stock_filter == "new_closing_highs" :
        cursor.execute("""
            SELECT * FROM (
                SELECT 
	                stock_prices.stock_id,
	                stock.symbol,
	                stock.name,
	                MAX(stock_prices.close) as price,
	                stock_prices.date
                FROM stock JOIN stock_prices
                ON stock.id = stock_prices.stock_id
                GROUP BY stock_id
            ) WHERE date = '2025-10-30'
            ORDER BY symbol ASC;
        """)
        rows = cursor.fetchall()

        return templates.TemplateResponse("stock_filter.html",{"request" : request , "stocks" : rows})
    elif stock_filter == "new_closing_lows" :
        cursor.execute("""
            SELECT * FROM (
                SELECT 
	                stock_prices.stock_id,
	                stock.symbol,
	                stock.name,
	                MIN(stock_prices.close) as price,
	                stock_prices.date
                FROM stock JOIN stock_prices
                ON stock.id = stock_prices.stock_id
                GROUP BY stock_id
            ) WHERE date = '2025-10-30'
            ORDER BY symbol ASC;
        """)
        rows = cursor.fetchall()

        return templates.TemplateResponse("stock_filter.html",{"request" : request , "stocks" : rows})
    elif stock_filter == "new_intraday_lows" :
        cursor.execute("""
            SELECT * FROM (
                SELECT 
	                stock_prices.stock_id,
	                stock.symbol,
	                stock.name,
	                MIN(stock_prices.low) as price,
	                stock_prices.date
                FROM stock JOIN stock_prices
                ON stock.id = stock_prices.stock_id
                GROUP BY stock_id
            ) WHERE date = '2025-10-30'
            ORDER BY symbol ASC;
        """)
        rows = cursor.fetchall()

        return templates.TemplateResponse("stock_filter.html",{"request" : request , "stocks" : rows})

    else :
        cursor.execute("SELECT symbol,name FROM stock ORDER BY symbol ASC")
        rows = cursor.fetchall()
        # this code will be used to return html page -> take refrence of jinja 2 website
        return templates.TemplateResponse("index.html" , {"request" : request , "stocks" : rows})
        # here, we returned html template , and this html template 
        # will have access to stocks which contain all info from rows
    


@app.get("/stock/{symbol}") # /{symbol} is taking symbol from the url
def stock_detail(request:Request , symbol): #passed symbol to the function
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    #stock_symbol_filter = request.query_params.get("filter",False)  # getting parameters from the url  

    # if stock_symbol_filter = "opening_range_breakout" :
    # elif stock_symbol_filter = "opening_range_breakdown" :
 
 
    # for showing strategies on the screen
    cursor.execute("""
        SELECT * FROM strategy
    """)
    strategies = cursor.fetchall()

    cursor.execute("""
        SELECT 
            stock.symbol,
            stock.name,
            stock.exchange,
            stock.id,
            stock_prices.date,
            stock_prices.open,
            stock_prices.close,
            stock_prices.high,
            stock_prices.low,
            stock_prices.volume
        FROM stock JOIN stock_prices
        ON stock.id = stock_prices.stock_id
        WHERE stock.symbol = ?
        ORDER BY stock_prices.date ASC
    """,(symbol,)) # here we require ',' becuase otherwise pyhton will not treat it like a tuple
    stock_symbols = cursor.fetchall()
    return templates.TemplateResponse("stockSymbol.html",{"request" : request , "stock_details" : stock_symbols , "strategies" : strategies})

# now , handle the post request -> we are posting the data to server and insert data in DB
#  we fetch the data using get request 
# to use this , we have to import the form from fast api

@app.post("/apply_strategy/")
def apply_strategy(strategy_id : int = Form(...),stock_id : int = Form(...)): #these are inputs to the function
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # we will now insert the stocks on which we have to apply certain strategies
    # in the stock_strategy table

    cursor.execute("""
        INSERT INTO stock_strategy 
            (stock_id,strategy_id)
            VALUES(?,?)
    """,(stock_id,strategy_id,))

    # save the changes
    connection.commit()

    # we will redirect the response 
    return RedirectResponse(url=f"/strategy/{strategy_id}",status_code=303)

# here , we successfully inserted data in the stock_strategy table
# now , we will show all the stocks in which strategies are being applied

@app.get("/strategy/{strategy_id}")
def strategy(request : Request,strategy_id):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name FROM strategy
        WHERE id = ?
    """, (strategy_id , ))

    # now i have fetched which strategy we have applied

    strategy = cursor.fetchone()

    cursor.execute("""
        SELECT 
            stock.symbol, stock.name
        FROM stock JOIN stock_strategy
        ON stock.id = stock_strategy.stock_id
        WHERE stock_strategy.strategy_id = ?
    """, (strategy_id, ))

    stocks = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request" : request, "stocks" : stocks , "strategy" : strategy})


@app.get('/stock/{stock_symbol}/latest_news')
def news(request : Request , stock_symbol):
    current_date = date.today()
    prev_day = current_date - timedelta(days=1)
    # make an api request to fetch the latest news 
    # Setup client
    finnhub_client = finnhub.Client(api_key=config.FINNHUB_KEY)

    # to fetch the news 
    news = finnhub_client.company_news(stock_symbol, _from = '2025-11-19' , to = '2025-11-20')
    
    if not news :   
        return templates.TemplateResponse("noNews.html",{"request":request , "errorStr" : 'NO LATEST NEWS AVAILABLE!!'})

    
    # formatting date is necessary : it is given in codeword
    for every in news:
        every['datetime'] = datetime.fromtimestamp(every['datetime'], tz=ZoneInfo("Asia/Kolkata"))
    return templates.TemplateResponse("stockNews.html",{"request":request , "stock_news" : news})
    

@app.get('/stock/{symbol}/stock_financials')
def details(request : Request , symbol):
    finnhub_client = finnhub.Client(api_key=config.FINNHUB_KEY)
    financials = finnhub_client.company_basic_financials(symbol, metric='all')
    if not financials:
        return templates.TemplateResponse("noNews.html",{"request" : request,"errorStr" : 'NO FINANCIAL DATA AVAILABLE!!'})

    return templates.TemplateResponse("stockFinancials.html" , {"request":request , "symbol" : symbol , "financials" : financials}  )


@app.get('/stock/{symbol}/assets')
def assests(request : Request , symbol):
    finnhub_client = finnhub.Client(api_key=config.FINNHUB_KEY)
    assets = finnhub_client.financials_reported(symbol=symbol,freq='all')
    if not assets['data']:
        return templates.TemplateResponse("noNews.html",{"request":request,"errorStr" : 'NO ASSETS DATA AVAIALBLE!!'})

    return templates.TemplateResponse("stockAssets.html",{"request":request,"stock_assets":assets , "symbol" : symbol})

@app.get('/stock/{symbol}/earnings')
def assests(request : Request , symbol):
    finnhub_client = finnhub.Client(api_key=config.FINNHUB_KEY)
    earnings = finnhub_client.company_earnings(symbol)
    if not earnings:
        return templates.TemplateResponse("noNews.html",{"request":request,"errorStr" : 'NO EARNINGS DATA AVAIALBLE!!'})

    return templates.TemplateResponse("stockEarnings.html",{"request":request,"stock_earnings":earnings , "symbol" : symbol})

@app.get('/stock/{symbol}/trends')
def assests(request : Request , symbol):
    finnhub_client = finnhub.Client(api_key=config.FINNHUB_KEY)
    trends = finnhub_client.recommendation_trends(symbol)
    if not trends:
        return templates.TemplateResponse("noNews.html",{"request":request,"errorStr" : 'NO TRENDS DATA AVAIALBLE!!'})

    return templates.TemplateResponse("trend.html",{"request":request,"trends":trends , "symbol" : symbol})