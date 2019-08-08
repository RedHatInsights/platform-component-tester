import config
import logging

def initialize_logging():
    kafkalogger = logging.getLogger("kafka")
    kafkalogger.setLevel("ERROR")
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(threadName)s %(levelname)s %(name)s - %(message)s"
    )

    logger = logging.getLogger(config.APP_NAME)

    return logger
