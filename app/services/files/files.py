import aioboto3

from fastapi import UploadFile

from config.conf import settings


async def upload_file_to_s3(file: UploadFile, image_path: str) -> str:
    session = aioboto3.Session()
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    async with session.resource("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key) as s3:
        bucket = await s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        await bucket.put_object(Body=file.file, Key=image_path, Metadata={"ACL": "public-read"})
        uploaded_file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_path}"
        return uploaded_file_url
