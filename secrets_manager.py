import json
import boto3


def retrieve_db_credentials(secret_name, region_name):
    """ Retrieves DB credentials from Secrets Manager
    :return: Dictionary containing DB connection credentials.
    """
    session = boto3.session.Session()
    secret = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value = secret.get_secret_value(SecretId=secret_name)
    secret_string = json.loads(get_secret_value.get('SecretString'))
    return secret_string
