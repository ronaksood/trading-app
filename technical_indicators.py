from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

import matplotlib.pyplot as plt


# this code is used to apply the indicators on a particular stock
# refer to alpha vantage python on google later



ti = TechIndicators(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ti.get_trima(symbol='MSFT', interval='60min', time_period=60)
data.plot()
plt.title('Trima indicator for  MSFT stock (60 min)')
plt.show()

# to show intraday chart using api
ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()