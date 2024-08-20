# filename: compare_stocks.py

import pandas_datareader.data as web
from datetime import datetime

def get_ytd_return(ticker):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        start_date = f"{today[:4]}-01-01"
        
        data = web.DataReader(ticker, 'yahoo', start_date, today)
        initial_price = data['Close'].iloc[0]
        final_price = data['Close'].iloc[-1]
        
        ytd_return = (final_price - initial_price) / initial_price * 100
        return ytd_return
    except Exception as e:
        print(f"Failed to get ticker '{ticker}': {e}")
        return None

meta_ytd_return = get_ytd_return("META")
tesla_ytd_return = get_ytd_return("TSLA")

if meta_ytd_return is not None:
    print(f"META YTD return: {meta_ytd_return:.2f}%")
else:
    print("Could not fetch META YTD return.")

if tesla_ytd_return is not None:
    print(f"Tesla YTD return: {tesla_ytd_return:.2f}%")
else:
    print("Could not fetch Tesla YTD return.")