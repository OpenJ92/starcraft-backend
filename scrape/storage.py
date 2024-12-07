import aiofiles
import boto3
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    async def save(self, file_name, data):
        """Save replay data."""
        pass

class AsyncLocalStorage(Storage):
    def __init__(self, directory):
        self.directory = directory

    async def save(self, file_name, data):
        file_path = f"{self.directory}/{file_name}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)
        print(f"Saved asynchronously: {file_path}")

class AsyncS3Storage(Storage):
    def __init__(self, bucket_name, folder=""):
        self.bucket_name = bucket_name
        self.folder = folder
        self.s3 = boto3.client("s3")

    async def save(self, file_name, data):
        key = f"{self.folder}/{file_name}" if self.folder else file_name
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)
        print(f"Uploaded asynchronously to S3: {self.bucket_name}/{key}")
