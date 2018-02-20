import json
import os
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])

    Response = table.query(
        ProjectionExpression="ts, answer, correct, first_number, second_number",
        KeyConditionExpression=Key('userid').eq(event["queryStringParameters"]["userid"]),
        Limit=10,
        ScanIndexForward=False
        )

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        },
        "body": json.dumps(Response["Items"], cls=DecimalEncoder),
        "isBase64Encoded": 0
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
