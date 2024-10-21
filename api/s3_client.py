import boto3
import botocore
from botocore.exceptions import NoCredentialsError

from config import (AWS_ACCESS_KEY, AWS_REGION, AWS_SECRET_KEY, AWS_BUCKET_NAME)

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
    endpoint_url="https://s3.storage.selcloud.ru"
)


def upload_to_s3(file):
    try:
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file.filename)
    except NoCredentialsError:
        return "Credentials not available"
    return file


def download_from_s3(file_name: str):
    try:
        s3_client.download_file(AWS_BUCKET_NAME, file_name, f"C:/Users/marmelad/Desktop/tetrika/{file_name}")
        return f"File {file_name} has been downloaded successfully"
    except botocore.exceptions.ClientError as e:
        return f"Error downloading file: {e}"


def delete_from_s3(file_name):
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_name)
        return f"File {file_name} has been deleted successfully"
    except botocore.exceptions.ClientError as e:
        return f"Error deleting file: {e}"
