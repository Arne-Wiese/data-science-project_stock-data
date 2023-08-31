import requests
import csv
import os

class AlphaVantageStockData:
    def __init__(self, api_key):
        self.api_key = api_key

    def extend_stock_data_csv(self, symbols):
        data_folder = 'data'
        os.makedirs(data_folder, exist_ok=True)
        
        csv_file_path = os.path.join(data_folder, "monthly_adjusted.csv")
        csv_exists = os.path.exists(csv_file_path)
        
        for symbol in symbols:
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