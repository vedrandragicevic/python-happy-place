import requests
import boto3
import json
import os

"""
    OAuth 2.0 is the industry-standard protocol for authorization. 
    The most common way of accessing OAuth 2.0 APIs is using a “Bearer Token”. 
    This is a single string which acts as the authentication of the API request, 
    sent in an HTTP “Authorization” header. The string is meaningless to clients using it, 
    and may be of varying lengths. Bearer tokens are a much simpler way of making API requests, 
    since they don’t require cryptographic signing of each request. The tradeoff is that all API requests 
    must be made over an HTTPS connection, since the request contains a plaintext token that could be used by 
    anyone if it were intercepted. The downside to Bearer tokens is that there is 
    nothing preventing other apps from using a Bearer token if it can get access to it.
"""


# Pulling secret from secrets manager
def retrieve_api_credentials(secret_name, region, system_name):
    """
    Retrieves API credentials from Secrets Manager
    :return: API KEY
    """
    session = boto3.session.Session()
    secret = session.client(service_name='secretsmanager', region_name=region)
    get_secret_value = secret.get_secret_value(SecretId=secret_name)
    secret_string = json.loads(get_secret_value.get('SecretString'))
    return secret_string.get(str(system_name))


def get_token(token_url, data, client_id, client_secret):
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False,
                                          auth=(client_id, client_secret))
    access_token_response = access_token_response.json()
    token = access_token_response.get('access_token')
    return token


region_name = os.environ.get('AWS_REGION')
secrets_manager_secret_name = os.environ.get('SECRET_NAME_CREDENTIALS')


def lambda_handler(event, context):

    system_name = ""
    # Function invoke to get the dict from secrets manager
    secret_dict = retrieve_api_credentials(secrets_manager_secret_name, region_name, system_name)

    # Dict parsing
    device_url = secret_dict.get('device_url')
    token_url = secret_dict.get('token_url')
    client_id = secret_dict.get('client_id')
    client_secret = secret_dict.get('client_secret')
    username = secret_dict.get('username')
    password = secret_dict.get('password')
    scope = secret_dict.get('scope')

    # Data dict for authorization
    data = {'grant_type': 'password', 'username': username, 'password': password, "scope": scope}

    # Fetching the Bearer token
    token = get_token(token_url, data, client_id, client_secret)

    # Headers authorization
    api_call_headers = {'Authorization': 'Bearer ' + token}

    # Get request example
    custom_url = "vexify"
    url_test = f"{device_url}{custom_url}"
    response = requests.get(url_test, headers=api_call_headers, verify=False)
    response = response.json()
