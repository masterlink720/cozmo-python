#!/usr/bin/env python3


import logging
import sys
import cozmo

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

logger = logging.getLogger('Cozmo: jw singer')


def panic(*args, code=1):
    logger.fatal(*args)
    sys.exit(code)


def connect(conn):
    logger.debug('Waiting for robot connection')
    run(conn.wait_for_robot())


def run(bot):
    """
    :param cozmo.Robot bot:
    :return:
    """

    logger.info('Bot connected')

    with open('bible.txt', mode='r') as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        bot.say_text(line, use_cozmo_voice=False, duration_scalar=0.7).wait_for_completed()


def main():
    logger.info('Setting up cozmo and connecting')
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(connect)
    except cozmo.ConnectionError as e:
        panic('Failed to connect to cozmo [{}]'.format(e))


if __name__ == '__main__':
    main()
