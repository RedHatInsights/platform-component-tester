import json
import logging
import config

from kafka import KafkaConsumer

logger = logging.getLogger(config.APP_NAME)


def init_consumer(topic):
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=config.BOOTSTRAP_SERVERS,
                             group_id="test_consumer",
                             value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                             retry_backoff_ms=1000,
                             )

    return consumer


def consume(topic):
    consumer = init_consumer(topic)
    logger.info("Consumer initialized")
    logger.info("Reading Topic: %s", topic)
    while True:
        for data in consumer:
            msg = data.value
            logger.info("request_id %s took %s seconds to traverse pup", msg["platform_metadata"]["request_id"], msg["platform_metadata"]["elapsed_time"])
