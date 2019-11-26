#!/usr/bin/env python3.6

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
from urllib.parse import urlparse, urljoin


import requests
from lxml import html


GLOBALS = {
    "base_url": "http://www.poorlydrawnlines.com/",
    "archive_url": "http://www.poorlydrawnlines.com/archive/",
    "comic_url_xpath": '//*[@class="content page"]/ul/li/a/@href',
    "comic_img_xpath": '//*[@class="wp-block-image size-large"]/img/@src',
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
        version: 0.1.1
"""}

COMIC_PATTERN = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')


def show_logo():
    bad_colors = ["BLACK", "LIGHTBLACK_EX", "RESET"]
    colorama.init(autoreset=True)
    codes = vars(colorama.Fore)
    colors = [codes[color] for color in codes if color not in bad_colors]
    colored_logo = [
        random.choice(colors) + line for line in GLOBALS["logo"].split("\n")]
    print("\n".join(colored_logo))


def read_json_data(file_name: str) -> list:
    with open(file_name, "r") as jf:
        data = json.load(jf)
    return data


def write_json_data(file_name: str, data_object: list):
    with open(file_name, "w") as jf:
        data = json.dump(data_object, jf, indent=4, sort_keys=True)


def getter(url: str, xpath: str) -> str:
    return html.fromstring(requests.get(url).content).xpath(xpath)


def fetch_online_archive() -> list:
    print(f"Checking the online archive...")
    archive = getter(GLOBALS["archive_url"], GLOBALS["comic_url_xpath"])
    return [url for url in archive if COMIC_PATTERN.match(url)]


def head_option(values: list) -> str:
    return next(iter(values), None)


def get_comic_img_url(url: str) -> str:
    return head_option(getter(url, GLOBALS["comic_img_xpath"]))


def process_url_to_dict(new_urls: list) -> dict:
    for new_url in new_urls:
        name = urlparse(new_url).path.split("/")[-1]
        year = int(urlparse(new_url).path.split("/")[3])
        month = int(urlparse(new_url).path.split("/")[4])
        yield {
            "comic_name": name.split(".")[0],
            "file_name": name,
            "year": year,
            "month": month,
            "comic_url": urljoin(GLOBALS["base_url"], name + "/"),
            "comic_img_url": new_url}


def update_database() -> list:
    old_json_data = read_json_data('data.json')
    online_archive = fetch_online_archive()
    if len(online_archive) > len(old_json_data):
        diff = len(online_archive) - len(old_json_data)
        print(f"Found {diff} new comic(s).")
        print(f"Updating...")
        new_comics = [get_comic_img_url(nc) for nc in online_archive[:diff]]
        new_comics_json = [url for url in process_url_to_dict(new_comics)]
        updated_data = old_json_data + new_comics_json
        write_json_data('data.json', updated_data)
        print(f"Done updating!")
        new_json_data = read_json_data('data.json')
        return new_json_data
    return old_json_data


def make_dir(dir_path):
    return os.makedirs(Path(dir_path), exist_ok=True)


def save_image(comic: dict):
    comic_name = comic["file_name"]
    comic_year_folder = os.path.join(
        GLOBALS["save_directory"], str(comic["year"]))
    make_dir(comic_year_folder)
    fn = Path(comic_year_folder) / comic_name
    print(f"Fetching: {comic_name}")
    with requests.get(comic["comic_img_url"], stream=True) \
            as img, open(fn, "wb") as output:
        copyfileobj(img.raw, output)


def download_comics_menu(comics_found: int) -> int:
    print(f"\nThe are {comics_found} comics in the database.")
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


def main():
    show_logo()
    pws_data = update_database()
    comics_to_download = download_comics_menu(len(pws_data))
    for comic in pws_data[::-1][:comics_to_download]:
        save_image(comic)


if __name__ == '__main__':
    main()
