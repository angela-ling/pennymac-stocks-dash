import aws_cdk as core
import aws_cdk.assertions as assertions

from pennymac_stocks_dash.pennymac_stocks_dash_stack import PennymacStocksDashStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pennymac_stocks_dash/pennymac_stocks_dash_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PennymacStocksDashStack(app, "pennymac-stocks-dash")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
