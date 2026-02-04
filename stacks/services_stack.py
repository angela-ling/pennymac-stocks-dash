from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_scheduler as scheduler,
    TimeZone,
    aws_scheduler_targets as targets,
    CfnOutput
)
from constructs import Construct
import os
from dotenv import load_dotenv

class ServicesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stock_table, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Ingestion Lambda Function
        load_dotenv()

        ingestion_function = _lambda.Function(
            self, "IngestionFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/ingestion"),
            environment={
                "TABLE_NAME": stock_table.table_name, 
                "MASSIVE_API_KEY": os.getenv("MASSIVE_API_KEY")
            }
        )
        # Give Lambda permission to write to the DynamoDB table
        stock_table.grant_write_data(ingestion_function)

        # Define the Schedule (5:00 PM EST / 22:00 UTC)
        scheduler.Schedule(self, "DailyStockSchedule",
            schedule=scheduler.ScheduleExpression.cron(
                minute="0",
                hour="17", # 5:00 PM EST
                day="*",
                month="*",
                time_zone=TimeZone.AMERICA_NEW_YORK 
            ),
            target=targets.LambdaInvoke(ingestion_function),
            description="Fetches stock winners every weekday at 5 PM New York time."
        )

