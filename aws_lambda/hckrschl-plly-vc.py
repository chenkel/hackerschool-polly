from __future__ import print_function

import base64
import json
import traceback
from random import randint

import boto3

polly_client = boto3.client('polly')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    voice_id = 'Marlene'  # Default
    if 'voice' in event["queryStringParameters"]:
        if 'Hans' or 'Marlene' or 'Vicki' in event["queryStringParameters"]['voice']:
            voice_id = event["queryStringParameters"]['voice']
    try:
        text_for_polly = event["queryStringParameters"]['text']
        if not text_for_polly:
            raise Exception('Bitte einen Text im text-Feld übergeben.')

        audio_response = polly_client.synthesize_speech(VoiceId=voice_id,
                                                        OutputFormat='mp3',
                                                        LanguageCode='de-DE',
                                                        Text=text_for_polly)
        mp3_file_name = ''
        if 'AudioStream' in audio_response:
            mp3_file_name = str(randint(0, 10000000000)) + '.mp3'
            mp3_file_path = '/tmp/' + mp3_file_name

            with open(mp3_file_path, 'wb') as mp3_file:
                mp3_file.write(audio_response['AudioStream'].read())
            s3.upload_file(mp3_file_path, 'polly-hackerschool', 'stimme/' + mp3_file_name,
                           ExtraArgs={'ACL': 'public-read'})

        body_return = {
            'audio_url': 'https://polly-hackerschool.s3.eu-central-1.amazonaws.com/stimme/' + str(mp3_file_name)}

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'isBase64Encoded': False,
            },
            'body': json.dumps(body_return)
        }

    except Exception as e:
        exception_type = e.__class__.__name__
        exception_message = str(e)

        api_exception_obj = {
            "isError": True,
            "type": exception_type,
            "message": exception_message,
            "traceback": traceback.format_exc()
        }
        api_exception_json = json.dumps(api_exception_obj)

        return {
            'statusCode': 400,
            'body': api_exception_json,
            'headers': {
                'Content-Type': 'application/json',
                'isBase64Encoded': False,
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            }
        }
