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
    site_bucket=data.site_bucket,
    env=cdk.Environment(account='797605901303', region='us-east-1'))

app.synth()
