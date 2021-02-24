import codecs, requests
from bs4 import BeautifulSoup

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

#limit the data to two weeks from the current date
data = data[:14]


print(data)
