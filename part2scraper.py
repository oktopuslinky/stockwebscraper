import codecs, requests, re
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick2_ohlc

#The project will be analyzing any stock for a certain period of time.

def take_input(input_type, input_disp_text):
    input_valid = False
    if input_type == "data_entries":
        while input_valid is False:
            try:
                user_input = int(input(input_disp_text + ": "))
                if user_input and user_input <= 100 and user_input > 0:
                    input_valid = True
            except:
                print("Please input a valid integer from 1-100")

def get_stock_data():
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

    return the_stock, data



def get_entry_number():
    input_valid = False
    while input_valid is False:
        try:
            amount_data = int(input("How many data entries would you like to see? (maximum 100):  "))
            if amount_data and amount_data <= 100 and amount_data > 0:
                input_valid = True
        except:
            print("Please input a valid integer from 1-100")

    return amount_data

def generate_table(data):
    stocks = PrettyTable()
    stocks.field_names = ["Date", "Open", "High", "Low", "Close", "Adj close", "Volume"]
    stocks.add_rows(data)
    return stocks

def generate_ohlc_data(data):
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

    return the_opens, the_closes, the_highs, the_lows

def get_avg(the_data):
    return sum(the_data)/len(the_data)

def generate_candlestick(the_opens, the_closes, the_highs, the_lows):
    fig, ax = plt.subplots()
    candlestick2_ohlc(ax, the_opens, the_closes, the_highs, the_lows, width=0.6, colorup='g', colordown='r', alpha=0.75)
    
    plt.xlabel(f'Days from {amount_data} day mark')
    plt.ylabel('Candle for each day')
    plt.title(f'Candlestick chart of {the_stock.upper()}')
    plt.show()


the_stock, data = get_stock_data()
amount_data = get_entry_number()

#limit the data to 14 entries from the current date
data = data[:amount_data]

#generate the table
stocks = generate_table(data)
print(stocks)

#get opens, closes, highs, lows, then their average
the_opens, the_closes, the_highs, the_lows = generate_ohlc_data(data)
opens_avg = get_avg(the_opens)
closes_avg = get_avg(the_closes)
highs_avg = get_avg(the_highs)
lows_avg = get_avg(the_lows)

#print averages
print(f'''
---

Average open: ${"{:.2f}".format(opens_avg)}
Average close: ${"{:.2f}".format(closes_avg)}
Average highs: ${"{:.2f}".format(highs_avg)}
Average lows: ${"{:.2f}".format(lows_avg)}''')

#graph the candlestick chart
generate_candlestick(the_opens, the_closes, the_highs, the_lows)