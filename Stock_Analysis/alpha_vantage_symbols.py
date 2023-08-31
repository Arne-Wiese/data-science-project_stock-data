import requests
import csv

class AlphaVantageSymbols:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_active_symbols(self):
        csv_url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={self.api_key}"
        
        with requests.Session() as s:
            download = s.get(csv_url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            
            active_symbols = [row[0] for row in my_list if row[6] == 'Active']
            return active_symbols
        

