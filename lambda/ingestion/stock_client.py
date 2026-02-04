# Function: connect to stock API
# Param: a list of stock tickers
# Returns: a dictionary 

import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_stock_data(api_key, ticker, date):
    url = f"https://api.massive.com/v1/open-close/{ticker}/{date}"
    params = {
        "adjusted": "true",
        "apiKey": api_key
    }

    try:
        logger.info(f"Fetching data for {ticker} on {date}")
        response = requests.get(url, params=params, timeout=5) # Always use a timeout!
        
        # This will raise an error for 4xx or 5xx responses
        response.raise_for_status() 
        
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {ticker}: {e}")
        return None

def fetch_all_tickers(api_key, ticker_list, date):
    """
    Orchestrates the fetching of all 6 tickers.
    """
    all_data = []
    for ticker in ticker_list:
        data = get_stock_data(api_key, ticker, date)
        if data and data.get("status") == "OK":
            all_data.append(data)
    
    return all_data

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    # 1. Load your local .env file
    load_dotenv()
    api_key = os.getenv("MASSIVE_API_KEY")
    
    # 2. Define your test parameters
    tickers = ["AAPL", "MSFT"]
    test_date = "2026-01-09"
    
    # 3. Call your function and print results
    print(f"--- Testing API Fetch for {test_date} ---")
    results = fetch_all_tickers(api_key, tickers, test_date)
    
    for stock in results:
        print(type(stock))
        # print(f"Symbol: {stock['symbol']} | Close: {stock['close']}")

"""
Massive API response format:
{
  "afterHours": 322.1,
  "close": 325.12,
  "from": "2023-01-09",
  "high": 326.2,
  "low": 322.3,
  "open": 324.66,
  "preMarket": 324.5,
  "status": "OK",
  "symbol": "AAPL",
  "volume": 26122646
}
"""