import psycopg2
from psycopg2 import Error
import logging
import sys
import os

logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        stream=sys.stdout,
        level=logging.INFO)
logger = logging.getLogger("rds_script")
logger.setLevel(logging.INFO)


db_credentials_dict = {"user": "user123"}


try:
    logger.info(f"CONNECTING TO AURORA POSTGRES DB...")
    # Connect to an existing Postgres database
    connection = psycopg2.connect(
        user=db_credentials_dict.get("user"),
        password=db_credentials_dict.get("password"),
        host=db_credentials_dict.get("host"),
        port=db_credentials_dict.get("port"),
        database=db_credentials_dict.get("database"),
    )
    connection.set_session(autocommit=True)

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    logger.info(f"LOGGING PostgreSQL SERVER INFORMATION: {connection.get_dsn_parameters()}.")
    # Executing a SQL query to test the connection
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    logger.info(f"YOU ARE SUCCESSFULLY CONNECTED TO - {record}.")

except (Exception, Error) as error:
    logger.error(f"ERROR WHILE CONNECTING TO PostgreSQL AURORA DB, ERROR: {error}.")
    raise error
   
# Select statement
cursor.execute("SELECT * from <schema>.<table_name>")
record = cursor.fetchall()
print("Result ", record)

# Insert statement
insert_query = """ INSERT INTO item (item_Id, item_name, purchase_time, price) VALUES (%s, %s, %s, %s)"""
item_purchase_time = datetime.datetime.now()
item_tuple = (12, "Keyboard", item_purchase_time, 150)
cursor.execute(insert_query, item_tuple)
connection.commit()
print("1 item inserted successfully")

# Execute SQL stored procedure
try:
    logger.info(f"EXECUTING SQL STORED PROCEDURE 'etl.sp_load({path}, None)'...")
    cursor.execute("CALL etl.sp_load(%s,%s)", (path, None))

except Error as e:
    logger.error(f"ERROR DURING SQL PROCEDURE: {e}.")
    raise e

# Fetching sproc return value (JSON object)
sproc_result_dict = cursor.fetchone()[0]
logger.info(f"SQL PROCEDURE RESULT: {sproc_result_dict}.")


# Close the connection to DB
if connection:
    cursor.close()
    connection.close()
    logger.info("PostgreSQL CONNECTION IS CLOSED.")
