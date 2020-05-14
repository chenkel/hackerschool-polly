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

        audio_response = polly_client.synthesize_speech(VoiceId=voice_id,
                                                        OutputFormat='pcm',
                                                        LanguageCode='de-DE',
                                                        Text=text_for_polly)
        if 'AudioStream' in audio_response:
            wave_file_path = '/tmp/speech.wav'
            with wave.open(wave_file_path, 'wb') as wav_file:
                wav_file.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
                wav_file.writeframes(audio_response['AudioStream'].read())

        with open("/tmp/speech.wav", "rb") as f:
            s = base64.b64encode(f.read()).decode("utf-8")

        viseme = polly_client.synthesize_speech(VoiceId='Hans',
                                                OutputFormat='json',
                                                LanguageCode='de-DE',
                                                Text=text_for_polly,
                                                SpeechMarkTypes=['sentence', 'viseme', 'word'])

        with open("/tmp/speech.json", "wb") as f:
            returned_viseme = viseme['AudioStream'].read()
            returned_viseme = returned_viseme.replace(b'\n', b',')
            viseme_new = b"".join([b'[', returned_viseme, b']'])
            viseme_new = viseme_new.replace(b',]', b']')
            print(viseme_new)
            f.write(viseme_new)

        with open("/tmp/speech.json", "rb") as f:
            v = base64.b64encode(f.read()).decode("utf-8")
        return_body = json.dumps({'audio': s, 'viseme': v})

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'isBase64Encoded': True,
            'body': return_body,
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
