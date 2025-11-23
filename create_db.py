import sqlite3 , config


# connecting to database using .connect()
connection = sqlite3.connect(config.DB_FILE)


# we will create a cursor throught which we will execute our sql queries

cursor = connection.cursor()


# and this cursor object has a execute() method by which we are going to execute our queries

cursor.execute("""
CREATE TABLE IF NOT EXISTS stock(
	id INTEGER PRIMARY KEY,
	symbol TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL,
    exchange TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_prices(
	id INTEGER PRIMARY KEY,
	stock_id INT ,
	date NOT NULL,
	open NOT NULL,
	high NOT NULL,
	low NOT NULL,
	close NOT NULL,
	volume NOT NULL,
	FOREIGN KEY (stock_id) REFERENCES stock(id) 
)
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS stock_price_minute(
        id INTEGER PRIMARY KEY,
        stock_id INTEGER,
    	date TEXT NOT NULL ,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL ,
        FOREIGN KEY(stock_id) REFERENCES stock(id)  
	)
""")


# to commit the changes in the database we will use commit() method 
connection.commit()