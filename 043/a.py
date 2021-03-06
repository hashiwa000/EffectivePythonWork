from threading import Lock
import logging
from contextlib import contextmanager

lock = Lock()
with lock:
    print('Lock is held')


def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)

@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


if __name__ == '__main__':
    with debug_logging(logging.DEBUG):
        print('Inside:')
        my_function()
    print('After:')
    my_function()

    with log_level(logging.DEBUG, 'my-log') as logger:
        logger.debug('This is my message!')
        logging.debug('This will not print.')
    logger = logging.getLogger('my-log')
    logger.debug('Debug will not print.')
    logger.error('Error will print.')
