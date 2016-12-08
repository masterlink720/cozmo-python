#!/usr/bin/env python3


import logging
import sys
from datetime import datetime
import time
import asyncio
from random import randint
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

    # frame = bytearray()
    # for pixel in range(1024):
    #     frame.append(randint(0, 1))
    # for row in range(screen_size[0]):
    #    for col in range(screen_size[1]):
    #        frame.append(randint(0, 1))

    # print('\n\nBytes: {}\n\n'.format(frame))
    # bot.display_oled_face_image(frame, 5000)
    # time.sleep(6)
    # return

    font = get_font(14)
    clear = [0] * 1024

    while True:
        img = Image.new(mode='L', size=screen_size, color=0)
        msg = ImageDraw.Draw(img)
        msg.multiline_text(text=get_now('   %a %b %w, %Y\n%H:%S'), font=font, fill=255,
                           xy=(0, 0), align='center', spacing=2)
        face = cozmo.oled_face.convert_image_to_screen_data(img)
        bot.display_oled_face_image(face, 1100)
        time.sleep(1)



def main():
    logger.info('Setting up cozmo and connecting')
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(connect)
    except cozmo.ConnectionError as e:
        panic('Failed to connect to cozmo [{}]'.format(e))


if __name__ == '__main__':
    main()
