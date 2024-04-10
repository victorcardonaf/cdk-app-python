import json
import boto3

ssm = boto3.client('ssm')

def on_event(event, context):
    data = json.loads(event)
    environment = data['environment']
    response = ssm.get_parameter(
    Name='/platform/account/env',
    WithDecryption=False)
    
    values = response['Parameter']['Value'].split(",")
    for value in values:
        if environment in value:
            if environment == "development":
                response = 1
                break
            else:
                response = 2
                break
            
    print(response)
    return response