# Hackerschool - Emoji Viseme with Amazon Polly 
## Lambdas
Both Python 3.8 functions are deployed and accessible with a GET method behind an API Gateway.

### aws_lambda/hckrschl-plly-spchmrks.py
Calls the Amazon Polly API to retrieve the speech marks with a given ```text``` and ```voice```. 
The result is returned as JSON.

### aws_lambda/hckrschl-plly-vc.py
Calls the Amazon Polly API to retrieve the synthesized speech with a given ```text``` and ```voice```. 
The result is a json['audio_url'] that links to the MP3 stored on an S3 bucket.

## Clients
### repl.it (under construction)
https://repl.it/@chenkel/PllyHckrschl
#### hackerschool-client.py (only used for initial testing)


## Getting started
Access the API Gateway endpoints for speech and speech marks and you are ready to go.