'''
Moody-Desktop Wallpaper Application
'''

__author__ = "Anvesh"
__version__ = "0.1"

import ctypes
import io
import logging
import os

import requests
from PIL import Image, ImageFilter
from screeninfo import get_monitors

from config import curr_dir, client_id, url

logging.basicConfig(filename="src/moody-desktop.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

log = logging.getLogger()
log.setLevel(logging.DEBUG)

photo_type = "photos/"
param = "random/"


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0), width=0, height=0):
    x, y = im.size
    if x > y:
        new_width = width
        new_height = new_width * y / x
    else:
        new_height = height
        new_width = new_height * x / y

    im = im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
    new_im = Image.new('RGB', (width, height), fill_color)
    new_im.paste(im, (int((width - new_width) / 2), int((height - new_height) / 2)))
    return new_im


def get_fnl_img_multi_monitor(file_name):
    monitors_lst = get_monitors()
    total_width = sum([x.width for x in monitors_lst])
    total_height = max([x.height for x in monitors_lst])
    fnl_img = Image.new('RGB', (total_width, total_height))
    for indx, item in enumerate(monitors_lst):
        img = get_rand_img_lnk()
        downl_img_byte = download_img(img, indx=indx, x=0, y=0)
        tmp_img = Image.open(io.BytesIO(downl_img_byte))
        fnl_img.paste(make_square(tmp_img, width=item.width, height=item.height), (item.x, item.y))

    fnl_img.save(os.path.join(curr_dir, file_name))
    return


def get_rand_img_lnk():
    '''
    Hit Unsplash url and return a photo link
    :return:
    '''
    response = requests.get(url + photo_type + param, params={"client_id": client_id()})
    if response.status_code != 200:
        log.error("API error")
        raise ConnectionError(response.json())
    return response.json()["urls"]["regular"]


def download_img(img, indx="", x=0, y=0):
    '''
    Download the image from the website
    :param img_url:
    :return:
    '''
    r = requests.get(img)
    return r.content


def set_wallpaper(downl_img_path):
    '''
    Set the wallpaper
    :param img_path:
    :return:
    '''
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(curr_dir, downl_img_path), 0)


def main():
    ''' All magic starts here'''
    log.info("Starting")
    file_name = r'img\temp.jpg'
    try:
        get_fnl_img_multi_monitor(file_name)
        set_wallpaper(file_name)
        log.info("file captured")
    except:
        log.error("Something went Wrong")






if __name__ == "__main__":
    '''When called start here'''
    main()
