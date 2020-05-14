# Hackerschool Polly Viseme
Das ist die Alpha

## Installation
```
pip install -r requirements.txt
```
## Components
### hackerschool-client.py (only use this when testing)
Calls the API and decodes the wav and viseme base64 encoded parts.

### aws_lambda/hackerschool-polly-api.py
Calls the Amazon Polly API to retrieve the wav of a given ```text``` and predefined ```voice```. Both results are returned in a json where the data is b64 encoded.

It is deployed as an AWS Lambda behind a GET method of an API Gateway.