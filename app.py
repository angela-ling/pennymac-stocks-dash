#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.services_stack import ServicesStack
from stacks.data_stack import DataStack

app = cdk.App()

data = DataStack(
    app, 
    "DataStack",
    env=cdk.Environment(account='797605901303', region='us-east-1'))
ServicesStack(
    app, 
    "ServicesStack", 
    stock_table=data.stock_table,
    env=cdk.Environment(account='797605901303', region='us-east-1'))


# PennymacStocksDashStack(app, "PennymacStocksDashStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.

#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.

#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */

#     env=cdk.Environment(account='797605901303', region='us-east-1'),

#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )

app.synth()
