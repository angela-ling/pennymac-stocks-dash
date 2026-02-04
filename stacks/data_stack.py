from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    CfnOutput,
    RemovalPolicy
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
        self.site_bucket = s3.Bucket(
            self, "StockAppBucket",
            public_read_access=True,    # Any browser can access the bucket
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True, # Ignore any Access Control Lists because they are file by file
                block_public_policy=False,  # Let people read the folder
                ignore_public_acls=True,    # Ignore any ACL. Don't want to make files public via ACL
                restrict_public_buckets=False   # ALlow folder to be labeled as public
            ),  # Make sure the bucket is publicly accessible
            website_index_document="index.html",
            removal_policy=RemovalPolicy.DESTROY,   # To avoid charges after interview is complete
            auto_delete_objects=True
        )

        # Output the Website URL
        CfnOutput(self, "WebsiteURL", value=self.site_bucket.bucket_website_url)
