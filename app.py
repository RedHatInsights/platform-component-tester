import traceback

import config
import tester_logging
import consumer
import producer
import maps


logger = tester_logging.initialize_logging()


def main():

    component_map = {"pup": maps.PUP}
    logger.info("Starting Component Tester")
    config.log_config()

    if config.ROLE == "consume":
        data = component_map[config.COMPONENT]
        consumer.consume(data["consume_topic"])
    elif config.ROLE == "produce":
        data = component_map[config.COMPONENT]
        producer.produce(data["produce_topic"], data["msg"])
    else:
        logger.error("Role not recognized: %s", config.ROLE)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        the_error = traceback.format_exc()
        logger.error(f"Platform Component Tester failed with Error: {the_error}")
