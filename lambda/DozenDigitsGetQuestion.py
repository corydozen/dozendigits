import random
import json

def lambda_handler(event, context):
    first_upper_bound = 50
    second_upper_bound = 20
    if event["queryStringParameters"]["difficulty"] == 'low':
        first_upper_bound = 10
        second_upper_bound = 10
    elif event["queryStringParameters"]["difficulty"] == 'medium':
        first_upper_bound = 50
        second_upper_bound = 11

    Question = {
        'first_number': random.randint(2,first_upper_bound),
        'second_number': random.randint(2,second_upper_bound)
    }

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        },
        "body": json.dumps(Question),
        "isBase64Encoded": False
    }
