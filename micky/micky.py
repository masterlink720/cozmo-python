#!/usr/bin/env python3


import logging
import sys
from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont
import cozmo

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

logger = logging.getLogger('Cozmo: clock face')


def panic(*args, code=1):
    logger.fatal(*args)
    sys.exit(code)


def connect(conn):
    logger.debug('Waiting for robot connection')
    run(conn.wait_for_robot())


def get_now(fmt='%A %b %w, %Y'):
    return datetime.now().strftime(fmt)


def get_font(size=8):
    return ImageFont.truetype('../ttf/roboto/Roboto-Regular.ttf', size=size)


def run(bot):
    """
    :param cozmo.Robot bot:
    :return:
    """

    logger.info('Bot connected')

    screen_size = cozmo.oled_face.dimensions()
    logger.info('Screen size, width: {}, height: {}'.format(screen_size[0], screen_size[1]))

    # Load micky
    logger.info('Opening micky.jpg and resizing')
    micky = Image.open('../img/micky.jpg').resize(screen_size)

    # Convert to cozmo-language
    face = cozmo.oled_face.convert_image_to_screen_data(micky)

    # GO GO GO
    logger.info('Displaying image for 5 seconds')
    bot.display_oled_face_image(face, 5000)
    time.sleep(5)


def main():
    logger.info('Setting up cozmo and connecting')
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(connect)
    except cozmo.ConnectionError as e:
        panic('Failed to connect to cozmo [{}]'.format(e))


if __name__ == '__main__':
    main()
