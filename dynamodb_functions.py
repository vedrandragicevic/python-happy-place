import boto3
from boto3.dynamodb.conditions import Key


dynamodb_client = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')


def create_dynamodb_table(table_name: str):
    params = dict(
        TableName=table_name,
        KeySchema=[

            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[

            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 196,
            'WriteCapacityUnits': 196
        }
    )

    table = dynamodb_resource.create_table(**params)
    print(f"Creating {table_name}...")
    table.wait_until_exists()
    return table


def get_records_from_dynamodb(table_name: str):
    all_records = dynamodb_client.describe_table(
        TableName=table_name
    )
    return all_records


def add_item_to_dynamodb_table(table_name: str, item_dict: dict):
    table = dynamodb_resource.Table(table_name)
    response = table.put_item(
        Item=item_dict
    )
    return response


def delete_table(table_name: str):
    # DELETE TABLE
    table = dynamodb_resource.Table(table_name)

    response = dynamodb_client.delete_table(
        TableName=table_name
    )
    print("DELETING TABLE...")
    table.wait_until_not_exists()
    return table


def query_dynamodb_by_pk(table_name, pk_column, pk_value):
    table = dynamodb_resource.Table(table_name)
    response = table.query(
        Select="ALL_ATTRIBUTES",
        KeyConditions={
            pk_column: {
                'AttributeValueList': [
                    pk_value
                ],
                'ComparisonOperator': 'EQ'
            }

        }
    )
    return response


def query_dynamodb_by_index(table_name, index_name, column_name, value):
    table = dynamodb_resource.Table(table_name)
    response = table.query(
            # Add the name of the index you want to use in your query
            IndexName=index_name,
            KeyConditionExpression=Key(column_name).eq(value),
        )
    return response


def query_dynamodb_by_pk2(table_name, pk_column, pk_value):
    """
    :param table_name: DynamoDB table name to query
    :param pk_column: Name of the primary key column
    :param pk_value: Value of the primary key
    :return: response: DynamoDB query response
    """
    table = dynamodb_resource.Table(table_name)
    response = table.query(KeyConditionExpression=Key(pk_column).eq(pk_value), ConsistentRead=True)
    return response


def update_dynamodb_item(table_name, pk_column, pk_value, sk_column, sk_value, atr_column, atr_value):
    """
    :param table_name: DynamoDB table name to query
    :param pk_column: Name of the primary key column
    :param pk_value: Value of the primary key
    :param sk_column: Name of the sort key column
    :param sk_value: Value of the sort key
    :param atr_column: Name of the attribute to update
    :param atr_value: New value of the attribute
    :return: response: DynamoDB query response
    """
    table = dynamodb_resource.Table(table_name)
    response = table.update_item(
        Key={
            pk_column: pk_value,
            sk_column: sk_value
        },
        AttributeUpdates={
            atr_column: {
                "Value": atr_value
            },
        },
    )
    return response
