from __future__ import print_function

import base64
import json
import traceback

import wave
import boto3

polly_client = boto3.client('polly')


def lambda_handler(event, context):
    voice_id = 'Marlene'  # Default
    if 'voice' in event["queryStringParameters"]:
        if 'Hans' or 'Marlene' or 'Vicki' in event["queryStringParameters"]['voice']:
            voice_id = event["queryStringParameters"]['voice']
    try:
        text_for_polly = event["queryStringParameters"]['text']
        if not text_for_polly:
            raise Exception('Bitte einen Text im text-Feld übergeben.')

        viseme = polly_client.synthesize_speech(VoiceId=voice_id,
                                                OutputFormat='json',
                                                LanguageCode='de-DE',
                                                Text=text_for_polly,
                                                SpeechMarkTypes=['sentence', 'viseme', 'word'])

        returned_viseme = viseme['AudioStream'].read()
        returned_viseme = returned_viseme.replace(b'\n', b',')
        viseme_new = b"".join([b'[', returned_viseme, b']'])
        viseme_new = viseme_new.replace(b',]', b']')
        print(viseme_new)
        viseme_return = viseme_new.decode("utf-8")

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': viseme_return,
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
                'isBase64Encoded': False
            }
        }
