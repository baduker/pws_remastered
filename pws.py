# pylint: disable=unnecessary-comprehension
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
import datetime
from pathlib import Path
from shutil import copyfileobj
from urllib.parse import urlparse, urljoin


import requests
import colorama
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
        version: 0.1.4
"""}

COMIC_PATTERN = re.compile(r"http://www.poorlydrawnlines.com/comic/.+")


def show_logo():
    bad_colors = ["BLACK", "LIGHTBLACK_EX", "RESET"]
    colorama.init(autoreset=True)
    codes = vars(colorama.Fore)
    colors = [codes[color] for color in codes if color not in bad_colors]
    logo = GLOBALS["logo"].split("\n")
    colored_logo = [random.choice(colors) + line for line in logo]
    print("\n".join(colored_logo))


def read_json_data(file_name: str) -> list:
    with open(file_name, "r") as jf:
        data = json.load(jf)
    return data


def write_json_data(file_name: str, data_object: list):
    with open(file_name, "w") as jf:
        json.dump(data_object, jf, indent=4, sort_keys=True)


def getter(url: str, xpath: str) -> list:
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
        year = extract_url_value(new_url, 3)
        month = extract_url_value(new_url, 4)
        yield {
            "comic_name": name.split(".")[0],
            "file_name": name,
            "year": year,
            "month": month,
            "comic_url": urljoin(GLOBALS["base_url"], name + "/"),
            "comic_img_url": new_url,
            }


def extract_url_value(url: str, position: int) -> int:
    return int(urlparse(url).path.split("/")[position])


def update_database() -> list:
    old_json_data = read_json_data('data.json')
    online_archive = fetch_online_archive()
    diff = len(online_archive) - len(old_json_data)
    if diff > 0:
        updated_data = old_json_data + get_new_comics(online_archive, diff)
        write_json_data('data.json', updated_data)
        new_json_data = read_json_data('data.json')
        print(f"Done updating!")
        return new_json_data

    return old_json_data


def get_new_comics(online_archive: list, diff: int) -> list:
    print(f"Found {diff} new comic(s).\nUpdating...")
    new_comics = (get_comic_img_url(comic) for comic in online_archive[:diff])
    return [url for url in process_url_to_dict(new_comics)]


def make_dir(dir_path: str):
    return os.makedirs(Path(dir_path), exist_ok=True)


def get_folder_name(comic: dict) -> str:
    comic_year = str(comic["year"])
    folder_name = os.path.join(GLOBALS["save_directory"], comic_year)
    return folder_name


def save_image(comic: dict):
    comic_name = comic["file_name"]
    folder = get_folder_name(comic)
    make_dir(folder)
    file_name = Path(folder) / comic_name
    print(f"Fetching: {comic_name}")
    with requests.get(comic["comic_img_url"], stream=True) \
            as img, open(file_name, "wb") as output:
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
        if comics_to_download == 0:
            sys.exit()
        return comics_to_download


def show_time(time_in_seconds: float) -> str:
    if isinstance(time_in_seconds, float):
        minutes, seconds = divmod(int(time_in_seconds), 60)
        hours, minutes = divmod(minutes, 60)
        human_readable_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return human_readable_time
    else:
        raise TypeError("Invalid time execution input.")


def get_comics(comics_to_download: int, pws_data: list):
    start = datetime.datetime.utcnow()
    for comic in pws_data[::-1][:comics_to_download]:
        save_image(comic)
    stop = datetime.datetime.utcnow()
    time_taken = show_time((stop - start).total_seconds())
    print(f"Downloaded {comics_to_download} comic(s) in {time_taken}")


def main():
    show_logo()
    pws_data = update_database()
    comics_to_download = download_comics_menu(len(pws_data))
    get_comics(comics_to_download, pws_data)


if __name__ == '__main__':
    main()
