import json
import time
import logging
import os
import boto3
import sys
import config


from kafka import KafkaConsumer, KafkaProducer

logger = logging.getLogger(config.APP_NAME)

if any("OPENSHIFT" in k for k in os.environ):
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
    AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")

    s3 = boto3.client("s3",
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

else:
    AWS_ACCESS_KEY_ID = os.getenv('MINIO_ACCESS_KEY', None)
    AWS_SECRET_ACCESS_KEY = os.getenv('MINIO_SECRET_KEY', None)
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', "http://minio:9000")

    s3 = boto3.client('s3',
                      endpoint_url=S3_ENDPOINT_URL,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


producer = KafkaProducer(bootstrap_servers=config.BOOTSTRAP_SERVERS,
                         value_serializer=lambda x: json.dumps(x).encode("utf-8")
                         )


def get_keys():
    keylist = []
    for key in s3.list_objects(Bucket=config.FETCH_BUCKET)["Contents"][:config.MSG_COUNT]:
        keylist.append(key["Key"])

    return keylist


def get_url(uuid):
    url = s3.generate_presigned_url("get_object",
                                    Params={"Bucket": config.FETCH_BUCKET,
                                            "Key": uuid}, ExpiresIn=86400)
    return url

def produce(topic, msg):
    keys = get_keys()
    for key in keys:
        url = get_url(key)
        msg["request_id"] = key
        msg["url"] = url
        logger.info("sending message for ID %s", key)
        producer.send(topic, value=msg)

    producer.flush()
