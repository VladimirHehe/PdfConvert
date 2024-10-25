import io
import boto3
import botocore
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile, HTTPException
from config import (AWS_ACCESS_KEY, AWS_REGION, AWS_SECRET_KEY, AWS_BUCKET_NAME)

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
    endpoint_url="https://s3.storage.selcloud.ru"
)


async def upload_to_s3(file: UploadFile, filename: str,):
    try:
        file_content = await file.read() if not isinstance(file, io.BytesIO) else file.read()
        file_obj = io.BytesIO(file_content)
        s3_client.upload_fileobj(file_obj, AWS_BUCKET_NAME, filename)
        # await push_pathS3_in_DB(AWS_BUCKET_NAME, filename)
        return filename
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credentials not available")


async def download_from_s3(file_name: str):
    try:
        local_path = f"C:/Users/marmelad/Desktop/tetrika/{file_name}"
        s3_client.download_file(AWS_BUCKET_NAME, file_name, local_path)
        return local_path
    except botocore.exceptions.ClientError as e:
        return f"Error downloading file: {e}"


async def delete_from_s3(file_name:str):
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_name)
        return f"File {file_name} has been deleted successfully"
    except botocore.exceptions.ClientError as e:
        return f"Error deleting file: {e}"
