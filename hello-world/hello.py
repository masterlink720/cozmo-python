#!/usr/bin/env python3


import logging
import sys
import cozmo

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

logger = logging.getLogger('Cozmo: Hello World')


def panic(*args, code=1):
    logger.fatal(*args)
    sys.exit(code)


def run(conn):
    logger.debug('Waiting for robot connection')
    bot = conn.wait_for_robot()

    logger.info('Bot connected')
    bot.say_text('Whats up world?').wait_for_completed()


def main():
    logger.info('Setting up cozmo and connecting')
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        panic('Failed to connect to cozmo [{}]'.format(e))


if __name__ == '__main__':
    main()
