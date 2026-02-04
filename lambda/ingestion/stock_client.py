# Function: connect to stock API
# Param: a list of stock tickers
# Returns: a dictionary 

import requests
import logging
import time

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
        response = requests.get(url, params=params, timeout=5) 

        # If the market was closed, this endpoint usually returns 404 or a specific message
        if response.status_code == 404:
            return {"status": "NOT_FOUND"}
        # raise an error for 4xx or 5xx responses
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

        # On holidays or weekends, if the API returns 'NOT_FOUND' or isn't 'OK', skip the whole day
        if not data or data.get("status") != "OK":
            logger.info(f"Market data not available for {date}. Likely a weekend or holiday.")
            return []
        
        all_data.append(data)

        # Rate limiting: 5 requests per minute = 12 seconds per request
        time.sleep(12)
    
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