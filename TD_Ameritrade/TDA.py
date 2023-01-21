import pprint
from td.client import TDClient
from datetime import datetime, timedelta

TD_ACCOUNT = '686104586'

# create a new instance of the client
TDSession = TDClient(client_id = 'EQ6BIF2SBCVDQHNGTJFBBRKUYT8OYIYC',
						redirect_uri = 'https://localhost/unfolio',
						credentials_path = '/Users/thomas/Desktop/testing_TD/td_state.json')

# Login to a new session
TDSession.login()

# Get current quotes
quotes_response = TDSession.get_quotes(instruments = ['MSFT','AAPL','SQ'])
# pprint.pprint(quotes_responses)

# Positions and Orders for an Account or Accounts
orders_and_positions = TDSession.get_accounts(account = TD_ACCOUNT,
												fields = ['positions', 'orders'])
# pprint.pprint(orders_and_positions)

# Grad all the transactions that meet a certain criteria
transactions = TDSession.get_transactions(account = TD_ACCOUNT,
							transaction_type = 'ALL',
							symbol = 'MSFT',
							start_date = '2020-01-01',
							end_date = '2020-04-01')

# market hours
# market_hours = TDSession.get_market_hours(markets=['BOND','FOREX'], date='2020-04-06')


opt_chain = {
	'symbol':'AAPL',
	'contract_type':'CALL',
	'optionType':'S',
	'fromDate':'2020-04-01',
	'afterDate':'2020-05-01',
	'strikeCount':4,
	'includeQuotes':True,
	'range':'ITM',
	'strategy':'ANALYTICAL',
	'volatility':29.0,
}
# get option chains
option_chains = TDSession.get_options_chain(option_chain = opt_chain)
## pprint.pprint(option_chains)

# Search Instruments - Symbol Search
search_instrument1 = TDSession.search_instruments(symbol = 'MSFT', projection = 'symbol-search')
## pprint.pprint(search_instrument1)

# Search Instruments - Search Regex
search_instrument2 = TDSession.search_instruments(symbol = 'M.*', projection = 'symbol-regex') # All that start with M
## pprint.pprint(search_instrument2)

# Search Instruments - Description
search_instrument3 = TDSession.search_instruments(symbol = 'quantum', projection = 'desc-search')
# pprint.pprint(search_instrument3)

# Search Instruments - Description Regex
search_instrument4 = TDSession.search_instruments(symbol = 'Technology.*', projection = 'desc-regex')
# pprint.pprint(search_instrument4)

# Search Instruments - Fundamental Data
search_instrument5 = TDSession.search_instruments(symbol = 'MSFT', projection = 'fundamental')
# pprint.pprint(search_instrument5)


# Get Instruments
instrument = TDSession.get_instruments(cusip = '594918104')
##pprint.pprint(instrument)


# Get Movers -> Only Returns something when market is open
dji_movers = TDSession.get_movers(market = '$DJI', direction = 'up', change = 'percent')
# pprint.pprint(dji_movers)


### Minute Data

## Define teh static arguments.
# hist_symbl = 'MSFT'
# hist_needExtendedHoursDate = False

## Define the dynamic arguments - I want 5 DAYS of historical 1 minute bars
# hist_periodType = 'day'
# hist_period = 5
# hist_frequencyType = 'minute'
# hist_frequency = 1

## Make the request
# historical_1_minute = TDSession.get_price_history(symbol = hist_symbol, periodType = hist_periodType, period = hist_period, frequency_type = hist_frequencyType, frequency = hist_frequency, extended_hours = hist_needExtendedHoursData)

# 1 minute chart - Max 30 days back
minute_date = TDSession.get_price_history(symbol='MSFT', period_type='day', period=5, frequency_type='minute', frequency=5, extended_hours=True)

# 5 minute chart
minute_date = TDSession.get_price_history(symbol='MSFT', period_type='day', period=5, frequency_type='minute', frequency=5, extended_hours=True)

# Daily Chart
# valid daily period month = [1,2,3,6] months of daily data
# valid daily period year = [1,2,3,5,10,15,20] years of daily data
# valid daily period ytd = [1] ytd of daily data
daily_data = TDSession.get_price_history(symbol='MSFT', period_type='month', period=6, frequency_type='daily', frequency=1, extended_hours=True) # 1 day bar for 6 months of daily data
# pprint.pprint(daily_data)


### Custom TimeRage

# Define 31 days ago and today (max lookback for minute data is 31 days)
today_00 = datetime.now()
today_ago = datetime.now() - timedelta(days = 31)

# Convert the days to a timestamp
hist_start_date = str(int(round(today_ago.timestamp()*1000)))
hist_end_date = str(int(round(today_00.timestamp()*1000)))

## Define the dynamic arguments - hist_period / Period is not needed!!
hist_periodType = 'day'
hist_frequencyType = 'minute'
hhist_frequency = 1

# Make the request for Custom Timerange
historical_custom = TDSession.get_price_history(symbol='MSFT', period_type='day', frequency_type='minute', start_date=hist_start_date, end_date=hist_end_date, frequency=1, extended_hours=True) # 31 days of minute-level data
pprint.pprint(historical_custom)