import os

import oss2
import requests


def upload_to_oss(object_name: str, content: str | bytes) -> str:
    auth = oss2.Auth(
        access_key_id=os.getenv('OSS_ACCESS_KEY_ID'),
        access_key_secret=os.getenv('OSS_ACCESS_KEY_SECRET')
    )
    endpoint = 'oss-cn-shanghai.aliyuncs.com'
    region = 'cn-shanghai'

    bucket_name = os.getenv('OSS_BUCKET_NAME') or "text2img"
    bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)
    bucket.put_object(f"retrival/{object_name}", content)
    return f"https://{bucket_name}.oss-cn-shanghai.aliyuncs.com/retrival/{object_name}"


def download_from_oss(file_url: str) -> str:
    response = requests.get(file_url)
    return response.text
