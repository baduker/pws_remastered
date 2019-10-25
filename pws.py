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
from urllib.parse import urlparse, urljoin


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
        version: alpha
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


def read_json_data():
    with open('data.json', 'r') as jf:
        data = json.load(jf)
    # flip the list to get the newest comics first
    return data


def getter(url, xpath):
    return html.fromstring(requests.get(url).content).xpath(xpath)


def fetch_online_archive():
    print(f"Checking the online archive...")
    archive = getter(GLOBALS["archive_url"], GLOBALS["comic_url_xpath"])
    return [url for url in archive if COMIC_PATTERN.match(url)]


def head_option(values):
    return next(iter(values), None)


def get_comic_img_url(url):
    return head_option(getter(url, GLOBALS["comic_img_xpath"]))


def process_url_to_dict(new_urls: list):
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


def main():
    show_logo()
    pws_data = read_json_data()
    online_archive = fetch_online_archive()

    if len(online_archive) > len(pws_data):
        diff = len(online_archive) - len(pws_data)
        print(f"Found {diff} new comic(s).")
        print(f"Updating...")
        updated = [i for i in process_url_to_dict(
            [get_comic_img_url(nc) for nc in online_archive[:diff]])]

        all_together = pws_data + updated

        with open("data.json", "w") as jf:
            data = json.dump(all_together, jf, indent=4, sort_keys=True)
        print(f"Done updating!")

    most_current_data = read_json_data()
    comics_to_download = download_comics_menu(len(most_current_data))
    for comic in most_current_data[::-1][:comics_to_download]:
        save_image(comic)


if __name__ == '__main__':
    main()
