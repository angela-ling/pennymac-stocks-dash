from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
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
        
        # Define Hello lambda function
        my_function = _lambda.Function(
            self, "ServicesHelloFunction",
            runtime = _lambda.Runtime.NODEJS_22_X,
            handler = "index.handler",
            code = _lambda.Code.from_inline(
                """
                exports.handler = async function(event) {
                    return {
                        statusCode: 200,
                        body: JSON.stringify('Hello World - Services Stack'),
                    };
                };
                """
            ),
        )

        my_function_url = my_function.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        CfnOutput(self, "myFunctionUrlOutput", value=my_function_url.url)
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "PennymacStocksDashQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
