import requests
import csv
import os

class AlphaVantageHelper:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_active_symbols(self):
        # Url to fetch all symbols
        url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={self.api_key}"
        
        with requests.Session() as s:
            all_symbols = s.get(url)
            decoded_content = all_symbols.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            
            # Get all symbols which are active
            active_symbols = [row[0] for row in my_list if row[6] == 'Active']
            return active_symbols
        

    def extend_stock_data_csv(self, symbols, folder, filename):
        # Create destination path for file
        data_folder = folder
        csv_file_path = os.path.join(data_folder, filename)
        os.makedirs(data_folder, exist_ok=True)
        csv_exists = os.path.exists(csv_file_path)
        
        for symbol in symbols:
            # Checks if symbol is already in csv file
            if AlphaVantageHelper.is_in_csv(symbol=symbol, folder=folder, filename=filename):
                continue

            # Url for monthly adjusted data
            csv_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={self.api_key}&datatype=csv"
            
            # Download and extract new CSV data
            response = requests.get(csv_url)
            if response.status_code == 200:
                new_csv_data = response.content.decode('utf-8')
                csv_data = response.content.decode('utf-8')
                
                # Process the new CSV data
                new_csv_lines = new_csv_data.strip().split('\n')
                new_csv_lines = [f"{symbol},{line}" for line in new_csv_lines[1:]]
                new_csv_data = '\n'.join(new_csv_lines)
                
                if csv_exists:
                    # Append new CSV data to existing data
                    with open(csv_file_path, 'a', newline='', encoding='utf-8') as outfile:
                        outfile.write("\n")  # Add a new line to separate data
                        outfile.write(new_csv_data)
                    print(f"CSV data for {symbol} extended in: {csv_file_path}")
                else:
                    # Create a new CSV file with the "symbol" column
                    with open(csv_file_path, 'w', newline='', encoding='utf-8') as outfile:
                        header_line = csv_data.split('\n')[0]
                        outfile.write(f"symbol,{header_line}\n")
                        outfile.write('\n'.join(new_csv_lines[1:]))
                    print(f"CSV data for {symbol} saved to: {csv_file_path}")
                    csv_exists = True
            else:
                print(f"Failed to download CSV data for {symbol}. Status code: {response.status_code}")


    @staticmethod
    def is_in_csv(symbol, folder, filename):
        data_folder = folder
        csv_file_path = os.path.join(data_folder, filename)

        if not os.path.exists(csv_file_path):
            return False

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as infile:
            for line in infile:
                if line.startswith(symbol + ','):
                    return True
        
        return False
    
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


