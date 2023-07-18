"""
    Run lambda on a daily schedule.
    dev: 9:30AM UTC

    PSYCOPG2 LAYER: https://pypi.org/project/aws-psycopg2/

"""
import psycopg2
import boto3
import datetime
import logging
import json
import sys
import os
from botocore.exceptions import ClientError
from sql_query import *

sns_client = boto3.client('sns')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

redshift_secret_arn = os.environ.get('REDSHIFT_SECRET_ARN')
redshift_alert_sns_arn = os.environ.get('REDSHIFT_ALERT_SNS_ARN')
env_name = os.environ.get('ENVIRONMENT_NAME')


def connect_to_redshift(credentials: dict):
    conn = psycopg2.connect(
        host=credentials.get('host'),
        port=credentials.get('port'),
        database='vex_edh',
        user=credentials.get('username'),
        password=credentials.get('password')
    )
    return conn


def execute_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result


def get_secret(secret_name: str) -> dict:
    secret_name = secret_name
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return json.loads(secret)


def lambda_handler(event, context):
    redshift_credentials = get_secret(redshift_secret_arn)
    logger.info(f"FETCHED REDSHIFT CREDENTIALS FROM {redshift_secret_arn} SECRET")

    conn = connect_to_redshift(redshift_credentials)
    logger.info(f"CONNECTED TO REDSHIFT SUCCESSFULLY.")

    # A list of stg tables for which we are checking if the data was loaded today
    stg_table_names = ['stg_vex_table1', 'stg_vex_table2']

    logger.info(f"CHECKING FOR {stg_table_names} IF THE DATA WAS LOADED TODAY.")

    not_loaded_tables = []

    results = execute_query(conn, query)
    logger.info(f"EXECUTED SQL SELECT QUERY TO CHECK THE LAST TIMESTAMP FOR ALL TABLES.")

    # Process the query results as needed
    for row in results:
        logger.info(row)

        table_name = row[0]
        timestamp_dt = row[1]

        # Checking if the timestamp load day is different that current day
        if table_name in stg_table_names:
            if timestamp_dt.day != datetime.datetime.now().day:
                logger.info(f"DATA FOR {table_name} NOT LOADED TODAY. LAST TIMESTAMP: {timestamp_dt}")
                not_loaded_tables.append(table_name)

    # Close DB connection
    conn.close()
    logger.info(f"CLOSED REDSHIFT DB CONNECTION.")

    # Send SNS
    if not_loaded_tables:
        message = f'List of tables that were not loaded today.\n \
            \t{not_loaded_tables}\n\n'

        logger.info(f"SENDING SNS MESSAGE: {message} TO TOPIC: {redshift_alert_sns_arn}")
        response = sns_client.publish(
            TargetArn=redshift_alert_sns_arn,
            Message=message,
            Subject=f'[REDSHIFT DATA LOAD ALERT] IN {env_name} ENV',
        )

    return {
        "MESSAGE": "SUCCESSFULLY CHECKED IF ALL REDSHIFT TABLES WERE LOADED WITH NEW DATA."
    }

