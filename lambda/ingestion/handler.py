import os
import logging
from stock_client import fetch_all_tickers
from processor import calculate_highest_mover
from database import save_winner_to_db
from datetime import datetime, timedelta, timezone

logger = logging.getLogger()

def handler(event, context):
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    api_key = os.environ.get("MASSIVE_API_KEY")
    table_name = os.environ.get('TABLE_NAME')

    # Determine Target Date (EST Logic)
    # Using UTC-5 (EST) standard library to avoid extra dependencies. Lambda runs in UTC by default.
    est = timezone(timedelta(hours=-5))
    now = datetime.now(est)

    # If triggered before 11 PM EST, look at yesterday's data
    # Reasoning: Massive should have data ready at midnight EST. Give one hour buffer for Massive API to update
    target_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')

    logger.info(f"Triggered at {now}. Targeting market date: {target_date}")
    
    try:
        # 1. Connect to Massive API
        raw_data = fetch_all_tickers(api_key, tickers, target_date)

        # 2. Calculate highest percent change
        winner = calculate_highest_mover(raw_data)

        # 3. Store in DynamoDB
        save_winner_to_db(table_name, winner)

    except ValueError as e:
            # Catch specific "Business Logic" errors you raised on purpose
            logger.warning(f"Validation Error: {e}")
            return {"statusCode": 400, "body": str(e)}
    except Exception as e:
            # Catch EVERYTHING else (The safety net)
            logger.error(f"Critical System Error: {e}", exc_info=True) # exc_info adds the stack trace
            return {"statusCode": 500, "body": "An internal error occurred."}
    
if __name__ == "__main__":
    # 1. Load your local .env file
    
    # 2. Call the handler function for local testing
    handler()