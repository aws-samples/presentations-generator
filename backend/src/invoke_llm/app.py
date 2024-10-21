import os
import boto3
import json
from datetime import datetime, timezone, timedelta

boto3_session = boto3.session.Session()
region = boto3_session.region_name
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["table_name"])

# create a boto3 bedrock client
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

# get knowledge base id from environment variable
kb_id = os.environ["kb_id"]

# declare model id for calling RetrieveAndGenerate API
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
model_arn = f'arn:aws:bedrock:{region}::foundation-model/{model_id}'

def retrieveAndGenerate(input, kbId, model_arn):
    print(input, kbId, model_arn)

    return bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': input
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kbId,
                'modelArn': model_arn
            }
        },
    )

def lambda_handler(event, context):
    prompt = "Você é um assistente de geração de apresentações de slides que auxilia professores nas aulas com os alunos e que receberá do solicitante o tema da apresentação que será {texto}. Caso o solicitante não informe o número de slides que deve ser gerado, você deverá gerar uma apresentação com 05 slides. Essa apresentação deverá conter informações como número do slide que deve ser inserida no campo sldnumber, o título do slide que deve ser inserido no campo sldtitle, um texto com a explicação sobre o conteúdo, que não gere nenhum conflito com as polices de responsabilidade de IA da AWS e que seja politicamente correto deverá ser inserido no campo sldcontent. A tradução do texto do campo sldcontent para inglês deve ser inserido no campo sldimgsuggestion."
    query = prompt.format(texto=event["question"])
    response = retrieveAndGenerate(query, kb_id, model_arn)
    generated_text = response['output']['text']
    sessionId = response['sessionId']
    retrieved_references = response.get('retrievedReferences', [])  # Obter as referências recuperadas

    slides_data = generated_text

    # Dividir o valor em slides individuais
    slides = slides_data.split('sldnumber:')

    # Criar a estrutura de dados para salvar no DynamoDB
    data = {
        "timestamp": datetime.now(timezone(timedelta(hours=-3))).isoformat(),
        "user_request": event["question"],
        "session_id": sessionId,
        "slides": []
    }

    # Processar cada slide e adicionar ao array de slides
    for slide in slides[1:]:
        slide_parts = slide.strip().split('\n')
        sldnumber = slide_parts[0]
        sldtitle = slide_parts[1].split('sldtitle:')[1].strip()
        sldcontent = slide_parts[2].split('sldcontent:')[1].strip()
        sldimgsuggestion = slide_parts[3].split('sldimgsuggestion:')[1].strip()

        slide_data = {
            "sldnumber": sldnumber,
            "sldtitle": sldtitle,
            "sldcontent": sldcontent,
            "sldimgsuggestion": sldimgsuggestion
        }
        data["slides"].append(slide_data)

    # Salvar os dados no DynamoDB
    table.put_item(Item=data)

    return {
        'statusCode': 200,
        'body': json.dumps('Slides saved to DynamoDB successfully!'),
        'session_id': sessionId,
        'response': response
    }