import boto3
import os
import uuid
import time
import json
import sys

def lambda_handler(event, context):
    try:
        first_number = json.loads(event['body'])['first_number']
        second_number = json.loads(event['body'])['second_number']
        user_id = str(json.loads(event['body'])['user_id'])
        if user_id is None:
            user_id = '1234'
        username = str(json.loads(event['body'])['username'])
        if username is None:
            username = '1234'
        answer = json.loads(event['body'])['answer']
        difficulty = json.loads(event['body'])['difficulty']

        #Inserting a new record in DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
        ts = time.gmtime()
        correct = int(first_number) * int(second_number) == int(answer)

        table.put_item(
            Item={
                'userid': user_id,
                'username': username,
                'ts': time.strftime("%Y-%m-%d %H:%M:%S", ts),
                'first_number': first_number,
                'second_number': second_number,
                'answer': answer,
                'correct': correct,
                'difficulty': difficulty
            }
        )

        Answer = {
            'correct': correct
        }
        if correct:
            payload = {
                'queryStringParameters': {
                    'difficulty': difficulty
                }
            }
            invoke_response = boto3.client('lambda').invoke(FunctionName="DozenDigitsGetQuestion",InvocationType="RequestResponse",Payload=json.dumps(payload))
            next_question = json.loads(invoke_response['Payload'].read())

            Answer["next_question"] = json.loads(next_question["body"])

        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : True
            },
            "body": json.dumps(Answer),
            "isBase64Encoded": False
        }
    except Exception, e:
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : True
            },
            "body": "Error " + str(e),
            "isBase64Encoded": False
        }


