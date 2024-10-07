import requests
import time
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY') #Either load the key here or just hardcode it

# Fill in the symbols needed
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'BRK.B', 'TSLA', 'META', 'UNH', 'XOM', 'JNJ', 'JPM', 'V', 'PG', 'MA', 'HD', 'CVX', 'PFE', 'LLY', 'KO']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# all months from 2001
for symbol in symbols:
    # Create an empty DataFrame for each symbol
    all_data = pd.DataFrame()

    for year in range(2001, 2024):
        for month in months:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&month={year}-{month}&outputsize=full&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()

            # Check if the response contains the expected data
            if "Time Series (1min)" in data.keys():
                time_series = data["Time Series (1min)"]
                df = pd.DataFrame.from_dict(time_series, orient='index')

                # Add the symbol and timestamp columns
                df['Timestamp'] = df.index
                df.insert(0, 'Symbol', symbol)

                # Rename columns for clarity
                df.columns = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Timestamp']

                # Reorder the columns
                df = df[['Timestamp', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']]


                all_data = pd.concat([all_data, df])

                # Pause to avoid hitting API rate limits
                time.sleep(0.5)
                print(f"Data found for {symbol} for {year}-{month}")
            else:
                print(f"Data not found for {symbol} for {year}-{month}")
                continue

    # Save the complete data for each symbol to a CSV file after collecting all months and years
    csv_file_path = f'{symbol}.csv'
    all_data.to_csv(csv_file_path, index=False)
    print(f"CSV file saved for {symbol}: {csv_file_path}")

