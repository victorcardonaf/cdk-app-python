#!/usr/bin/env python3

import aws_cdk as cdk
import os

from my_first_cdk_app.my_first_cdk_app_stack import MyFirstCdkAppStack

# env_us = cdk.Environment(account="939468338567", region="us-east-1")

app = cdk.App()
MyFirstCdkAppStack(app, "MyFirstCdkAppStack")
app.synth()
