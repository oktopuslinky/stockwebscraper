import codecs, requests, re
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.ticker as ticker
import datetime as datetime
import numpy as np

#The project will be analyzing the gme stock over 1 month.

'''
USEFUL PAGES:
https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
https://hackersandslackers.com/scraping-urls-with-beautifulsoup/

https://finance.yahoo.com/quote/GME/history/
'''

#ensures that the stock selected by user exists.
stock_valid = False
while stock_valid is False:
    the_stock = str(input("What stock do you want to analyze? (input stock ticker symbol): "))

    url = f'https://finance.yahoo.com/quote/{the_stock}/history/'
    req = requests.get(url)

    data = []
    soup = BeautifulSoup(req.content, "html.parser")
    the_rows = soup.find('tbody')
    
    #checks if:
    # Stock exists
    # There is data for a said stock 
    if soup.title.text.lower() != "symbol lookup from yahoo finance" and len(the_rows) > 0:
        stock_valid = True
    else:
        print("This stock does not exist or its data is not available. Please try again.")
        print("An example of a valid answer would be GME, the stock ticker symbol for GameStop.")

#get all the data and put it into a list of lists
for row in the_rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # get rid of empty values

#limit the data to 14 entries from the current date
data = data[:14]
stocks = PrettyTable()
stocks.field_names = ["Date", "Open", "High", "Low", "Close", "Adj close", "Volume"]
stocks.add_rows(data)

print(stocks)

'''
dates = list()

#gets the numerical date in the month from the date in the table

year = input("What is the current year?: ")
for the_date in data:
    the_string = the_date[0]
    
    the_string = the_string.strip(year)
    the_string = the_string.strip(str(int(year)-1))
    the_string = the_string.strip(str(int(year)+1))

    #removes all non-digits, commas, and decimals
    the_string = re.sub("[^\d\.]", "", the_string)
    dates.append(int(the_string))

#reverses dates from oldest to newest for graph
dates.reverse()
print(dates)
'''

the_opens = list()
for an_item in data:
    the_open = an_item[1]
    the_opens.append(float(the_open))

the_closes = list()
for an_item in data:
    the_close = an_item[2]
    the_closes.append(float(the_close))

the_highs = list()
for an_item in data:
    the_high = an_item[3]
    the_highs.append(float(the_high))

the_lows = list()
for an_item in data:
    the_low = an_item[4]
    the_lows.append(float(the_low))

the_opens.reverse()
the_closes.reverse()
the_highs.reverse()
the_lows.reverse()

print(the_opens)
print(the_closes)
print(the_highs)
print(the_lows)


'''
print(type(data[1][1]))

dates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
'''
print(data)

fig, ax = plt.subplots()
candlestick2_ohlc(ax, the_opens, the_closes, the_highs, the_lows, width=0.6, colorup='g', colordown='r', alpha=0.75)

#candlestick2_ohlc(ax, the_opens, data[2], data[3], data[4], width=0.6)
'''
xdate = [datetime.datetime.fromtimestamp(i) for i in dates]

ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
def mydate(x,pos):
    try:
        return xdate[int(x)]
    except IndexError:
        return ''

ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

fig.autofmt_xdate()
fig.tight_layout()
'''
plt.xlabel('Days from 14 day mark')
plt.ylabel('Candle for each day')
plt.title(f'Candlestick chart of {the_stock.upper()}')
plt.show()


'''plt.plot(dates, the_opens, 'ro')
plt.show()'''