import boto3
import requests

s3_client = boto3.client('s3')

# OBJECT_NAME_TO_UPLOAD = input("File name: ")
bucket_name = 'test_bucket1'
OBJECT_NAME_TO_UPLOAD = "target.csv"
names_list = ['geography', 'target']


# Get table name from names list
table_name = [item for item in names_list if item.split('-')[-1] in OBJECT_NAME_TO_UPLOAD][0]


# Generate the presigned URL
response = s3_client.generate_presigned_post(
    Bucket=bucket_name,
    Key=f"core/ins/extract/{table_name}/{OBJECT_NAME_TO_UPLOAD}",
    ExpiresIn=3600
)

print(response)

# Upload file to S3 using presigned URL
files = {
    'file': open(OBJECT_NAME_TO_UPLOAD, 'rb')
}
r = requests.post(response['url'], data=response['fields'], files=files)
print(r.status_code)

