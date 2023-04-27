import json
import boto3
from botocore.exceptions import ClientError, ConnectTimeoutError
from botocore.config import Config


def retrieve_db_credentials(secret_name, region_name, logger):
    """Retrieves DB credentials from Secrets Manager
    :return: Dictionary containing DB connection credentials.
    """
    # Config dict for retries
    boto_config = Config(
        connect_timeout=1,
        retries={
            "max_attempts": 5,
            "mode": "standard"
        }
    )

    secret_string = None

    session = boto3.session.Session()
    secret = session.client(service_name="secretsmanager", region_name=region_name, config=boto_config)

    # Connecting to SM and retrieving the secret
    try:
        get_secret_value = secret.get_secret_value(SecretId=secret_name)
        secret_string = json.loads(get_secret_value.get("SecretString"))
        logger.info(f"SUCCESSFULLY RETRIEVED DATABASE CREDENTIALS USING SM: {secret_string}")
    except ConnectTimeoutError as connection_timeout_error:
        logger.error(f"CONNECTION TIMEOUT ERROR WHEN CONNECTING TO SM: {connection_timeout_error}")
    except ClientError as client_error:
        logger.error(f"CLIENT ERROR WHEN CONNECTING TO SM: {client_error}")

    return secret_string
