import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup

class SymbolFetcher:
    def get_nasdaq_symbols(self):
        headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
        res=requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100",headers=headers)
        main_data=res.json()['data']['data']['rows']

        # Initialize an empty list to collect symbols
        symbols = []

        for i in range(len(main_data)):
            symbol = main_data[i]['symbol']
            symbols.append(symbol)

        return symbols

    def get_dow_jones_symbols(self):
        try:
            url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            #  Send GET request
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            #  Get the symbols table
            tables = soup.find_all('table')
            #  #  Convert table to dataframe
            df = pd.read_html(str(tables))[1]
            #  Cleanup
            df.drop(columns=['Notes'], inplace=True)
            return df
        except:
            print('Error loading data')
            return None
        
    def get_stoxx_europe_50_symbols(self):
        try:
            url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            #  Send GET request
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            #  Get the symbols table
            tables = soup.find_all('table')[4]
            #  #  Convert table to dataframe
            df = pd.read_html(str(tables))[0]
            return df
        except:
            print('Error loading data')
            return None