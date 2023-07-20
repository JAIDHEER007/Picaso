import boto3

import logging
logger = logging.getLogger('watchtower-logger')

from django.conf import settings
import os

class AwsManager:
    s3Bucket = boto3.resource(
        service_name = 's3',    
        region_name = settings.AWS_REGION,
        aws_access_key_id = settings.AWS_ACCESS_KEY,
        aws_secret_access_key = settings.AWS_SECERT_ACCESS_KEY
    ).Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    def upload_file(filename, key):
        try:
            logger.info("S3 Move Started")
            AwsManager.s3Bucket.upload_file(
                Filename = filename,
                Key = key, 
                ExtraArgs = {
                    'ContentType': "image/png"
                }
            )

            return True
        except Exception as e:
            logger.error(e)
        return False
    
    def delete_file(filename):
        try:
            AwsManager.s3Bucket.Object(filename).delete()
            return True
        except Exception as e:
            logger.error(e)
        return False