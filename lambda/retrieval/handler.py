import boto3
import os
import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from boto3.dynamodb.conditions import Attr # Important for filtering

# DecimalEncoder to prevent JSON crashes
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
    table_name = os.environ.get('TABLE_NAME')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # 1. Calculate the date range (Last 7 Days) We use last 10 days to account for weekends
    est = timezone(timedelta(hours=-5))
    end_date = datetime.now(est).strftime('%Y-%m-%d')
    start_date = (datetime.now(est) - timedelta(days=10)).strftime('%Y-%m-%d')

    try:
        # 2. Scan the table for dates within that range
        # We use Attr().between() to find all 7 items at once
        response = table.scan(
            FilterExpression=Attr('date').between(start_date, end_date)
        )
        
        items = response.get('Items', [])

        # 3. Sort them so the newest winner is at the top
        items.sort(key=lambda x: x['date'], reverse=True)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" # Required for your Frontend
            },
            "body": json.dumps(items, cls=DecimalEncoder)
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}