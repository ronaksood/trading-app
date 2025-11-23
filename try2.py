import finnhub

import config

from datetime import date , datetime , timezone


finnhub_client = finnhub.Client(api_key=config.FINNHUB_KEY)

current_date = date.today()

# news = finnhub_client.company_basic_financials('MSFT','all')

print(finnhub_client.recommendation_trends('AAPL'))

