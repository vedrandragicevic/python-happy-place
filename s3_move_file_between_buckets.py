import json
import boto3
from botocore.exceptions import ClientError, ConnectTimeoutError
from botocore.config import Config


def move_file_from_source_to_target_bucket(source_bucket: str, source_key: str, target_bucket: str, target_key: str):
    """
    Moves file from one S3 bucket to another S3 bucket.
    :param source_bucket: Source bucket to copy from
    :param source_key: File path in source bucket
    :param target_bucket: Target bucket to copy to
    :param target_key: File path in target bucket
    """
    session = boto3.Session()
    s3_resource = session.resource("s3", config=boto3.session.Config(connect_timeout=10, retries={'max_attempts': 3}))
    s3_client = boto3.client("s3", config=boto3.session.Config(connect_timeout=10, retries={'max_attempts': 3}))
    
    # Creating s3 source dict for copying file between buckets
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_key
    }

    # Move file between buckets
    s3_resource.meta.client.copy(copy_source, target_bucket, target_key)
    s3_client.delete_object(Bucket=source_bucket, Key=source_key)
