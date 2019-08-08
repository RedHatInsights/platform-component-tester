import os
import logging

APP_NAME = os.getenv("APP_NAME", "component-tester")

logger = logging.getLogger(APP_NAME)

def log_config():
    import sys
    for k, v in sys.modules[__name__].__dict__.items():
        if k == k.upper():
            if "AWS" in k.split("_"):
                continue
            logger.info("Using %s: %s", k, v)


ROLE = os.getenv("ROLE", "consume")
COMPONENT = os.getenv("COMPONENT", "pup")
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:29092").split()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MSG_COUNT = os.getenv("MSG_COUNT", 100)
FETCH_BUCKET = os.getenv("FETCH_BUCKET", "insights-upload-perma")
