import os
import boto3
import io
import base64
import json

bedrock_runtime_client = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["table_name"])
Bucket = os.environ["bucket_name"]

def lambda_handler(event, context):
    session_id = event['session_id']

    # Consulta no DynamoDB com base no session_id
    response = table.get_item(Key={'session_id': session_id})
    print(response)

    if 'Item' in response:
        item = response['Item']
        slides = item.get('slides', [])

        for slide in slides:
            sldimgsuggestion = slide.get('sldimgsuggestion', '')
            sldnumber = slide.get('sldnumber', '')
            print(sldimgsuggestion)

            if sldimgsuggestion:
                # Invocar o Amazon Bedrock com o prompt
                prompt = f"An image of {sldimgsuggestion}"
                seed = "0"
                base64_image_data = invoke_titan_image(prompt, seed)
                image_data = base64.b64decode(base64_image_data)
                object_key = f"generated_images/{session_id}/image_{sldnumber}.jpeg"

                s3.put_object(
                    Bucket=Bucket,
                    Key=object_key,
                    Body=image_data,
                    ContentType='image/jpeg'
                )   
                print(f"Imagem '{object_key}' salva no bucket S3.")
        else:
                print(f"Nenhuma descrição para geração de imagem encontrada no slide {sldnumber}")


        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"Imagens salvas com sucesso no bucket {Bucket}."}),
            'session_id': session_id
        }

    return {
        'statusCode': 404,
        'body': json.dumps({'message': f"Não foi possível encontrar dados para o session_id '{session_id}'."}),
        'session_id': session_id
    }
    
def invoke_titan_image(prompt, seed):
    request = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": prompt},
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "cfgScale": 10,
            "height": 1152, # Permissible sizes: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html#:~:text=The%20following%20sizes%20are%20permissible.
            "width": 768,
            "seed": 2000,
        },
    })

    response = bedrock_runtime_client.invoke_model(
        modelId="amazon.titan-image-generator-v1", body=request
    )

    response_body = json.loads(response["body"].read())
    base64_image_data = response_body["images"][0]

    return base64_image_data