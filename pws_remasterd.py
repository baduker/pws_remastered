#!/usr/bin/python3

"""
A simple image downloader for poorlydrawnlines.com/archive
"""
import os
import re
import sys
import time


import requests
from bs4 import BeautifulSoup as bs


DEFAULT_DIR_NAME = "poorly_created_folder"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)
ARCHIVE_URL = "http://www.poorlydrawnlines.com/archive/"
COMIC_PATTERN = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')


LOGO = """
                                                   _               _ 
  a comical web-scraper                           | |             | |
  _ ____      _____   _ __ ___ _ __ ___   __ _ ___| |_ ___ _ __ __| |
 | '_ \ \ /\ / / __| | '__/ _ \ '_ ` _ \ / _` / __| __/ _ \ '__/ _` |
 | |_) \ V  V /\__ \ | | |  __/ | | | | | (_| \__ \ ||  __/ | | (_| |
 | .__/ \_/\_/ |___/ |_|  \___|_| |_| |_|\__,_|___/\__\___|_|  \__,_|
 | |             ______
 |_|            |______|                    version: beta | June 2019

"""


def show_logo():
    print(LOGO)


# loads list of image source urls
def upload_source_urls():
    with open("data.bdkr", "r") as data:
        source_urls = data.readlines()
    # reverses the list to show comics from the most recent one
    return [line[:-1] for line in source_urls][::-1]


# reports on differences between the datebase and the online archive
def compare_database_with_the_archive(datebase, archive):
    db_len = len(datebase)
    arch_len = len(archive)
    difference = arch_len - db_len

    print("There are {} comics available in the datebase.".format(db_len))
    print("There are {} comics on the site.".format(arch_len))

    if difference > 1:
        print("There are {} new comics!".format(difference))
    elif difference == 1:
        print("There is {} new comic!.".format(difference))
    else:
        print("Bad news - there are no new comics.")
        print("Good news - you're datebase is up-to-date! :)")


def update_source_url(list_of_new_source_urls):
    return 0


# creates a default download folder
def create_folder():
    os.makedirs(DEFAULT_DIR_NAME, exist_ok=True)


# chops off the tail of source url to get a comic name
def get_comic_name(url):
    return url.split("/")[-1]


def check_for_new_comics(session):
    """
    Grabs all urls from the poorlydrawnlines.com/archive,
    parses for only those that link to published comics
    and returns an up-to-date list of all comics.
    """
    response = session.get(ARCHIVE_URL)
    soup = bs(response.text, 'html.parser')
    comics = [url.get("href") for url in soup.find_all("a")]
    return [url for url in comics if COMIC_PATTERN.match(url)]


def grab_image_src_url(session, url):
    """
    Fetches urls with the comic image source
    """
    response = session.get(url)
    soup = bs(response.text, 'html.parser')
    for div in soup.find_all('div', class_="post"):
        for figure in div.find_all('figure', class_="wp-block-image"):
            for img in figure.find_all('img', src=True):
                return img['src']


# fetches the comic image from the comic server
def download_comic(list_of_source_urls):
    session = requests.Session()
    for url in list_of_source_urls:
        print("Getting: {comic_name}".format(comic_name=get_comic_name(url)))
        save_comic(session, url)


# stores the comic image on the drive in the default folder
def save_comic(session, url):
    create_folder()
    file_name = get_comic_name(url)
    with open(os.path.join(COMICS_DIRECTORY, file_name), "wb") as comic_image:
        response = session.get(url)
        comic_image.write(response.content)


# one functions to rule them all!
def main():
    show_logo()

    session = requests.Session()

    pws_archive = check_for_new_comics(session)
    local_datebase = upload_source_urls()

    compare_database_with_the_archive(local_datebase, pws_archive)

    # UNCOMMENT TO START DOWNLOADING!
    # download_comic()


if __name__ == '__main__':
    main()
