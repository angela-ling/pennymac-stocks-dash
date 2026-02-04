from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_scheduler as scheduler,
    TimeZone,
    aws_scheduler_targets as targets,
    aws_apigateway as apigateway,
    aws_s3_deployment as s3_deploy,
    CfnOutput
)
from constructs import Construct
import os
from dotenv import load_dotenv

class ServicesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stock_table, site_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Ingestion Lambda Function
        load_dotenv()

        ingestion_function = _lambda.Function(
            self, "IngestionFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/ingestion"),
            timeout=Duration.minutes(2),
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

        # Retrieval Lambda Function
        retrieval_function = _lambda.Function(
            self, "RetrievalFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda/retrieval"),
            environment={
                "TABLE_NAME": stock_table.table_name
            }
        )

        # Grant Read Permissions
        stock_table.grant_read_data(retrieval_function)

        # API Gateway
        api = apigateway.RestApi(self, "StockApi", 
            rest_api_name="Stock Movers Service",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS
            }
        )

        winners_resource = api.root.add_resource("winners")

        # Connect retrieval_function
        winners_resource.add_method(
            "GET", 
            apigateway.LambdaIntegration(retrieval_function)
        )

        # Deploy the frontend files to the bucket created in DataStack
        s3_deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3_deploy.Source.asset("./frontend")],
            destination_bucket=site_bucket
        )





