import os
import json
import boto3
from datetime import datetime
import unicodedata

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('table_name')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    items = []
    scan_response = table.scan()
    print(f"Resposta do scan: {scan_response}")
    items.extend(scan_response['Items'])
    print(f"Itens obtidos: {items}")

    filtered_items = []
    for item in items:
        session_id = item.get('session_id', '')
        timestamp_str = item.get('timestamp', '')
        user_request = item.get('user_request', '')
        output_filename = item.get('output_filename', '')

        # Verificar se os campos existem antes de adicionar
        if session_id and timestamp_str and user_request:
            # Parse the timestamp string
            timestamp = datetime.fromisoformat(timestamp_str)

            # Convert the timestamp to the desired format
            formatted_timestamp = timestamp.strftime('%d/%m/%y - %H:%M')

            # Remove accents and non-ASCII characters from user_request
            user_request = unicodedata.normalize('NFKD', user_request).encode('ASCII', 'ignore').decode()

            filtered_item = {
                'session_id': session_id,
                'timestamp': formatted_timestamp,
                'user_request': user_request,
                'output_filename': output_filename
            }
            filtered_items.append(filtered_item)
            print(f"Item filtrado adicionado: {filtered_item}")
        else:
            print(f"Campos ausentes em: {item}")

    print(f"Itens filtrados: {filtered_items}")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
        "body": json.dumps(filtered_items),
    }