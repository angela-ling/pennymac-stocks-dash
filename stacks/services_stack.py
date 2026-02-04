from aws_cdk import (
    Stack,
    Duration,
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
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": stock_table.table_name, 
                "MASSIVE_API_KEY": os.getenv("MASSIVE_API_KEY")
            }
        )
        # Give Lambda permission to write to the DynamoDB table
        stock_table.grant_write_data(ingestion_function)

        # EventBridge cron job (5:00 PM EST)
        # Reasoning: Stock market closes at 4pm EST. Give one hour buffer for Massive API to update
        scheduler.Schedule(self, "DailyStockSchedule",
            schedule=scheduler.ScheduleExpression.cron(
                minute="0",
                hour="1", # 1:00AM EST or 10PM PST
                day="*",
                month="*",
                time_zone=TimeZone.AMERICA_NEW_YORK 
            ),
            target=targets.LambdaInvoke(ingestion_function),
            description="Fetches stock winners every weekday at 1:00 AM EST (10:00 PM PST) for the day that just ended."
        )

        # # Retrieval Lambda Function
        # retrieval_function = _lambda.Function(
        #     self, "RetrievalFunction",
        #     runtime=_lambda.Runtime.PYTHON_3_11,
        #     handler="handler.handler",
        #     code=_lambda.Code.from_asset("lambda/retrieval"),
        #     environment={
        #         "TABLE_NAME": stock_table.table_name
        #     }
        # )

        # # Grant Read Permissions
        # stock_table.grant_read_data(retrieval_function)

        # # Create a Function URL to visit it in browser
        # retrieval_url = retrieval_function.add_function_url(
        #     auth_type=_lambda.FunctionUrlAuthType.NONE, # Open to the public for the demo
        # )

        # # 4. Output the URL so you can find it after deploying
        # CfnOutput(self, "RetrievalApiUrl", value=retrieval_url.url)




