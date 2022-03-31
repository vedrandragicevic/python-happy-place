import pandas
import pandas_schema
import json
from pandas_schema import Column
from pandas_schema.validation import *
import numpy as np
import os
from typing import Tuple, List


def check_null(value):
    """
    Schema Validation Function that checks for null values in a given column.
    :param value: column value.
    :return: BOOL VALUE TRUE OR FALSE.
    """
    if value is not np.nan:
        return True
    else:
        return False


def pass_function(value):
    """
    Schema Validation Function that always return True.
    :param value: column value.
    :return: BOOL VALUE TRUE.
    """
    return True


def create_schema_object(schema_dict: dict) -> pandas_schema.schema.Schema:
    """
    Schema dict provides a list of rules that are used for validation.
        Supported rules:
            null_validation,
            always_pass,
            leading_whitespace_validation,
            range_validation,
            date_validation.
    These rules can be expanded with more custom or pandas schema built-in functions.
    Returns a 'Schema' object ->
        class pandas_schema.schema.Schema(columns: Iterable[pandas_schema.column.Column])
    :param schema_dict: schema dictionary
    :return: schema object
    """
    # Defining custom validation elements
    # class pandas_schema.validation.CustomElementValidation(validation: Callable[[Any], Any], message: str)
    null_validation = CustomElementValidation(lambda f: check_null(f), 'NULL value detected!')
    always_pass = CustomElementValidation(lambda f: pass_function(f), 'ALWAYS PASS!')

    column_object_list = list()

    # Adding validation methods (custom or built-in) to 'valid_method_list'
    for field in schema_dict.get('fields'):
        valid_method_list = list()
        for valid_method in field.get('rules'):
            if valid_method == 'null_validation':
                valid_method_list.append(null_validation)
            if valid_method == 'always_pass':
                valid_method_list.append(always_pass)
            if valid_method == 'leading_whitespace_validation':
                valid_method_list.append(LeadingWhitespaceValidation(message="Leading whitespace found!"))
            if valid_method == 'range_validation':
                valid_method_list.append(InRangeValidation(min=1, max=5, message="Value is not in the range!"))
            if valid_method == 'date_validation':
                valid_method_list.append(DateFormatValidation(date_format="%d/%m/%Y",
                                                              message="Date is not in specified format!"))

        # Creating column objects
        # class pandas_schema.column.Column(name: str, validations: Iterable[pandas_schema.validation._
        # BaseValidation] = [], allow_empty=False)
        column_object_list.append(pandas_schema.column.Column(field.get('name'), valid_method_list))

    schema = pandas_schema.schema.Schema(column_object_list)
    return schema


def do_validation(pandas_data: pd.DataFrame, schema: pandas_schema.schema.Schema) -> Tuple[List, List, List]:
    """
    Validates pandas df according to a schema object.
    Returns a tuple of 3 lists.
    First list contains error messages. Second list provides a row in df for the same index on the error message.
    Third list provides a column in df for the error message.

    :param pandas_data:pandas dataframe.
    :param schema: schema object.
    :return: Returns a tuple of 3 lists.
    """

    # APPLYING VALIDATION FOR THE INPUT DF
    errors = schema.validate(pandas_data)
    errors_index_rows = [e.row for e in errors]
    errors_index_columns = [e.column for e in errors]
    errors_index_messages = [e.message for e in errors]
    return errors_index_messages, errors_index_rows, errors_index_columns


def main():
    with open("validation_schema.json", "r") as file:
        validation_schema_dict = json.loads(file.read())

    validation_df = pandas.read_csv("validation_file.csv")

    pandas_schema_object = create_schema_object(validation_schema_dict)

    error_messages, errors_rows, errors_index_columns = do_validation(validation_df, pandas_schema_object)

    for error in range(0, len(error_messages)):
        print(f"Message: {error_messages[error]} Row: {errors_rows[error]}, Column: {errors_index_columns[error]}!")
        """
            OUTPUT:
                Message: Value is not in the range! Row: 2, Column: RangeTest!
                Message: Date is not in specified format! Row: 4, Column: ScanTimestamp!
                Message: Value is not in the range! Row: 4, Column: RangeTest!
        """


if __name__ == '__main__':
    main()
