from logging import getLogger, Formatter, INFO, StreamHandler, Logger


def get_logger(name):
    log_format = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
    logger = getLogger(name)
    formatter = Formatter(fmt=log_format)
    handler = StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(INFO)
    logger.addHandler(handler)
    return logger
