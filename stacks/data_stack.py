from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    CfnOutput
    # aws_sqs as sqs,
)
from constructs import Construct

class DataStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define DynamoDB table
        self.stock_table = dynamodb.TableV2(
            self, 
            "StockTable",
            partition_key = dynamodb.Attribute(name="date", type=dynamodb.AttributeType.STRING),
            billing = dynamodb.Billing.on_demand(),
        )

        # Define S3 bucket


        # Define lambda function
        my_function = _lambda.Function(
            self, "DataHelloFunction",
            runtime = _lambda.Runtime.NODEJS_22_X,
            handler = "index.handler",
            code = _lambda.Code.from_inline(
                """
                exports.handler = async function(event) {
                    return {
                        statusCode: 200,
                        body: JSON.stringify('Hello World - Data Stack'),
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
