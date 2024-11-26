import logging

from config import MODE


HANDLER = logging.StreamHandler()
HANDLER.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

def get_logger(name, mode=MODE):
    """Return logger with given name,
    level (mode), default formatting
    mode should be "debug", "test" or
    "work", by default its taken
    from the config MODE variable
    """
    logger = logging.getLogger(name)

    if mode == 'debug' or mode == 'test':
        logger.setLevel(logging.DEBUG)
    elif mode == 'work':
        logger.setLevel(logging.INFO)
    else:
        raise Exception('Bad mode parameter! Should be: "test", "debug" or "work"')

    logger.addHandler(HANDLER)
    return logger
