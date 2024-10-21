import os
import json
import boto3

BUCKET = os.environ["bucket_name"]
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    file_name = event['queryStringParameters']['filename']
    print(file_name)

    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': BUCKET,
            'Key': file_name
        },
        ExpiresIn=3600,
        HttpMethod='GET'
    )

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
        'body': json.dumps({
            'presigned_url': presigned_url
        })
    }