import sqlite3 , config

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy(
        id INTEGER PRIMARY KEY,
        name NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategy(
        stock_id INTEGER NOT NULL,
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY(stock_id) REFERENCES stock(id),
        FOREIGN KEY(strategy_id) REFERENCES strategy(id)         
    )
""")


# now we are going to populate our startegy tables

strategies = ["Opening_Range_Breakout","Opening_Range_Breakdown" , "Swing_Breakdown" , "Swing_Breakout" , "Reversal_Intraday"]

for strategy in strategies :
    cursor.execute("INSERT INTO strategy(name) VALUES(?)",(strategy,)) 
    # , is very imp otherise it will treat as individual chars

# populating strategy_stocks tables

# cursor.execute("""
#     INSERT INTO 
# """)

connection.commit()