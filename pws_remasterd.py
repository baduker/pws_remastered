#!/usr/bin/python3.6

######################################################
#
# pws - an image scraper for poorlydrwanlines.com
# written by baduker | github.com/baduker
# echo YmFkdWtlckBwcm90b25tYWlsLmNoCgo= | base64 -d
#
######################################################

import os
import re
import sys
import json
import random
import colorama
from pathlib import Path
from shutil import copyfileobj

import requests
from lxml import html


GLOBALS = {
    "base_url": "http://www.poorlydrawnlines.com/",
    "archive_url": "http://www.poorlydrawnlines.com/archive/",
    "comic_url_xpath": '//*[@class="content page"]/ul/li/a/@href',
    "comic_img_xpath": '//*[@class="wp-block-image"]/img/@src',
    "save_directory": "poorly_created_folder",
    "logo": """
a remake of...
┌─┐┌─┐┌─┐┬─┐┬ ┬ ┬
├─┘│ ││ │├┬┘│ └┬┘
┴  └─┘└─┘┴└─┴─┘┴
┬ ┬┬─┐┬┌┬┐┌┬┐┌─┐┌┐┌
│││├┬┘│ │  │ ├┤ │││
└┴┘┴└─┴ ┴  ┴ └─┘┘└┘
┌─┐┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
└─┐│  ├┬┘├─┤├─┘├┤ ├┬┘
└─┘└─┘┴└─┴ ┴┴  └─┘┴└─
        version: beta
"""}


def show_logo():
    bad_colors = ["BLACK", "LIGHTBLACK_EX", "RESET"]
    colorama.init(autoreset=True)
    codes = vars(colorama.Fore)
    colors = [codes[color] for color in codes if color not in bad_colors]
    colored_logo = [
        random.choice(colors) + line for line in GLOBALS["logo"].split("\n")]
    print("\n".join(colored_logo))


def read_json_data():
    with open('pws_data.json', 'r') as jf:
        data = json.load(jf)
    # flip the list to get the newest comics first
    return data[::-1]


def download_comics_menu(comics_found: int) -> int:
    print(f"\nThe scraper has found {comics_found} comics.")
    print("How many comics do you want to download?")
    print("Type 0 to exit.")
    while True:
        try:
            comics_to_download = int(input(">> "))
        except ValueError:
            print("Error: expected a number. Try again.")
            continue
        if comics_to_download > comics_found or comics_to_download < 0:
            print("Error: incorrect number of comics to download. Try again.")
            continue
        elif comics_to_download == 0:
            sys.exit()
        return comics_to_download


def make_dir():
    return os.makedirs(Path(GLOBALS["save_directory"]), exist_ok=True)


def save_image(comic: dict):
    comic_name = comic["file_name"]
    fn = Path(GLOBALS["save_directory"]) / comic_name
    print(f"Fetching: {comic_name}")
    with requests.get(comic["comic_img_url"], stream=True) \
            as img, open(fn, "wb") as output:
        copyfileobj(img.raw, output)


def main():
    show_logo()
    pws_data = read_json_data()
    comics_to_download = download_comics_menu(len(pws_data))
    make_dir()
    for comic in pws_data[:comics_to_download]:
        save_image(comic)


if __name__ == '__main__':
    main()
