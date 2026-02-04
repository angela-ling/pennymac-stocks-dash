import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()

def save_winner_to_db(table_name, winner_data):
    # 1. Initialize the DynamoDB Resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        # 2. Put the item into the table
        # DynamoDB is schemaless, but we must provide the Partition and Sort Keys
        logger.info(f"Saving {winner_data['symbol']} to table {table_name}")
        
        response = table.put_item(
            Item={
                'date': winner_data['from'],               # Sort Key
                'ticker': winner_data['symbol'],    # Convert numbers to strings or decimals
                'percent_change': winner_data['percent_change'],
                'close_price': winner_data['close']
            }
        )
        return response

    except ClientError as e:
        # 3. Handle AWS-side errors (permissions, throttling, etc.)
        logger.error(f"AWS Error saving to DynamoDB: {e.response['Error']['Message']}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in database.py: {e}")
        raise e
    
"""
{
    'status': 'OK', 
    'from': '2026-02-02', 
    'symbol': 'AAPL', 
    'open': 260.03, 
    'high': 270.49, 
    'low': 259.205, 
    'close': 270.01, 
    'volume': 73907067.0, 
    'afterHours': 268.77, 
    'preMarket': 258, 
    'percent_change': 3.84
}
"""