import os
import yfinance as yf


class Yahoohelper:
    def extend_stock_data_csv(self, symbols, folder, filename, start_date, end_date):
        # Create destination path for file
        data_folder = folder
        csv_file_path = os.path.join(data_folder, filename)
        os.makedirs(data_folder, exist_ok=True)
        csv_exists = os.path.exists(csv_file_path)

        # Specify the symbol and date range
        start_date = start_date
        end_date = end_date
        
        for symbol in symbols: 
            try:
                # Fetch historical data
                data = yf.download(symbol, start=start_date, end=end_date, interval="1mo")
                # List of columns to drop (Open, Close, High, Low, Volume)
                columns_to_drop = ['Open', 'Close', 'High', 'Low', 'Volume']
                # Drop the specified columns
                data.drop(columns=columns_to_drop, inplace=True)
                csv_data = data.to_csv()
                new_csv_data = data.to_csv()
                
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
                        outfile.write('\n'.join(new_csv_lines))
                    print(f"CSV data for {symbol} saved to: {csv_file_path}")
                    csv_exists = True
            except Exception as e:
                print("An error occured while fetching data:", str(e))