from aws_cdk import (
        Stack,
        assertions
        
    )
from my_first_cdk_app.my_first_cdk_app_stack import MyFirstCdkAppStack

import aws_cdk as cdk

# env_us = cdk.Environment(account="939468338567", region="us-east-1")

app = cdk.App()

def test_lambda_function():
    stack = MyFirstCdkAppStack(app, "test")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::Lambda::Function", {
      "Runtime": "python3.12"
    })
