""" This module provides access to DynamoDB class  """
import time
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr
import ast


class DynamoDB:
    def __init__(self, table_name: str, logger):
        """
        Init function.
        :param table_name: DynamoDB table name.
        :param logger: Variable for printing output.
        """
        self.dynamodb_client = boto3.client('dynamodb')
        self.dynamodb_resource = boto3.resource('dynamodb')
        self.table_name = table_name
        self.logger = logger
        self.table_object = self.dynamodb_resource.Table(table_name)


    def describe_table(self):
        """ Returns DynamoDB table metadata. """
        self.logger.info(f"Fetching DynamoDB table {self.table_name} metadata.")
        response = self.dynamodb_client.describe_table(
            TableName=self.table_name
        )
        return response


    def get_all_table_records(self):
        """ Returns all records from DynamoDB table. """
        self.logger.info(f"Fetching all records from DynamoDB table {self.table_name}.")
        response = self.table_object.scan()
        return response


    def add_item_to_table(self, item_dict: dict):
        """
        Adds new row into DynamoDB table.
        :param item_dict: Dictionary containing row data.
        :return: Response containing metadata and status code.
        """
        self.logger.info(f"Adding new row into DynamoDB table {self.table_name}.")
        try:
            response = self.table_object.put_item(
                Item=item_dict
            )
            return response
        except Exception as e:
            self.logger.exception(f"Error occurred when adding new row: {e}")
            raise e


    def update_table_row(self, pk_column: str, pk_value: str, sk_column: str, sk_value: str,
                         atr_column: str, atr_value):
        """
        Updates DynamoDB table attribute column with the attribute value.
        If the given primary key and sort key columns and values don't exist, 'update_item' method appends new row
        to the table.
        :param pk_column: Name of the primary key column
        :param pk_value: Value of the primary key
        :param sk_column: Name of the sort key column
        :param sk_value: Value of the sort key
        :param atr_column: Name of the attribute to update
        :param atr_value: New value of the attribute
        :return: response: DynamoDB update item response.
        """
        self.logger.info(f"Updating table row, column: {atr_column}, value: {atr_value}.")
        try:
            response = self.table_object.update_item(
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
        except Exception as e:
            self.logger.exception(f"Error occurred when updating row, error: {e}")
            raise e


    def query_table_by_primary_key(self, pk_column: str, pk_value: str):
        """
        Queries DynamoDB table based on the provided Primary Key column and Primary Key value.
        Query method returns all items with that Primary Key value.
        Another option is to use 'query' method with these parameters:
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
        :param pk_column: Name of the Primary Key column.
        :param pk_value: Value of the Primary Key.
        :return: response: DynamoDB Query response.
        """
        self.logger.info(f"Querying table with primary key column: {pk_column}, value: {pk_value}.")
        try:
            response = self.table_object.query(KeyConditionExpression=Key(pk_column).eq(pk_value), ConsistentRead=True)
            return response
        except Exception as e:
            self.logger.exception(f"Error occurred when querying table by primary key: {pk_column}, "
                                  f"value: {pk_value}, error: {e}")
            raise e


    def get_records_with_filter_condition(self, attribute_name: str, attribute_value: str):
        """
        Returns one or more items and item attributes by accessing every item in a table. Filters data
        after it is retrieved. Queries table based on attribute name and value provided.
        Possible filtering conditions:
            - between(low_value, high_value)
            - eq(value)
            - gt(value)
            - gte(value)
            - lt(value)
            - lte(value)
        :param attribute_name: Name of the attribute you want to apply filter to.
        :param attribute_value: Value of that attribute you're filtering.
        :return: DynamoDB Query response with metadata and items.
        """
        self.logger.info(f"Querying DynamoDB table based on attribute: {attribute_name}, value: {attribute_value}.")
        response = self.table_object.scan(
            FilterExpression=Attr(attribute_name).eq(attribute_value)
        )
        if not response.get('Items'):
            self.logger.info(f"No records founds for given attribute: {attribute_name}, value: {attribute_value}.")
        return response


    def query_table_by_global_index(self, index_name: str, column_name: str, value: str):
        """
        Queries DynamoDB table based on Global Secondary Index. A Global Secondary Index allows you to query attributes
        that are not part of the main table’s primary key and this will help you to avoid the slowness
        and inefficiencies that are associated when performing a full table scan operation.
        :param index_name: Name of the Global Index you want to query on.
        :param column_name: Name of the Table column you want to query on.
        :param value: Value of the Global Index you're searching for.
        :return: DynamoDB Query response with metadata and items.
        """
        self.logger.info(f"Querying DynamoDB table {self.table_name} based on Global index: "
                         f"{index_name}, value: {value}.")
        try:
            response = self.table_object.query(
                IndexName=index_name,
                KeyConditionExpression=Key(column_name).eq(value),
            )
            if not response.get('Items'):
                self.logger.info(f"No records found for index: {index_name}, column: {column_name}, "
                                 f"column value: {value}")
            return response
        except Exception as e:
            self.logger.exception(f"Error occurred when querying table with index: {index_name}, column: {column_name}, "
                                  f"column value: {value}, error: {e}")
            raise e


    def delete_table_row(self, pk_column: str, pk_value: str, sk_column: str, sk_value: str):
        """
        Deletes row in DynamoDB table based on primary key and sort key column names and values.
        :param pk_column: Name of the primary key column
        :param pk_value: Value of the primary key
        :param sk_column: Name of the sort key column
        :param sk_value: Value of the sort key
        :return: DynamoDB delete item response.
        """
        try:
            response = self.table_object.delete_item(
                Key={
                    pk_column: pk_value,
                    sk_column: sk_value
                }
            )
            return response
        except Exception as e:
            self.logger.exception(f"Error occurred when deleting row, error: {e}")
            raise e


    def create_dynamodb_table_backup(self, backup_name: str):
        """Creates DynamoDB table backup. """
        self.logger.info(f"Creating DynamoDB table backup with backup name: {backup_name}.")
        response = self.dynamodb_client.create_backup(
            TableName=self.table_name,
            BackupName=backup_name
        )
        return response


    def delete_dynamodb_table(self):
        """ Deletes DynamoDB table. """
        try:
            response = self.dynamodb_client.delete_table(
                TableName=self.table_name,
            )
            self.logger.info(f"DynamoDB table {self.table_name} was deleted successfully.")
            return response
        except Exception as e:
            self.logger.exception(f"Error occurred when deleting table {self.table_name}: {e}")
            raise e
