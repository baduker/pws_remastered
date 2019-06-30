#!/usr/bin/python3

"""
A simple image downloader for poorlydrawnlines.com/archive
"""
import os
import re
import sys
import time
import shutil
import datetime


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
 |_|            |______|                   version: alpha | July 2019

"""


def show_logo():
    print(LOGO)


# loads list of image source urls
def upload_source_urls():
    with open("data.bdkr", "r") as data:
        source_urls = data.readlines()
    # reverses the list to show comics from the most recent one
    # Actually, don't reverse it!
    return [line[:-1] for line in source_urls]


def count_difference(database, archive):
    return len(archive) - len(database)


# creates a default download folder
def create_folder():
    os.makedirs(DEFAULT_DIR_NAME, exist_ok=True)


# used to zip the comic download folder and the database
def zip_it(zip_name, folder_name):
    today = datetime.date.today()
    full_zip_name = zip_name + "_" + str(today)
    shutil.make_archive(full_zip_name, "zip", folder_name)


# chops off the tail of source url to get a comic name
def get_comic_name(url):
    return url.split("/")[-1]


def check_online_archive(session):
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
def download_comic(list_of_source_urls, comics_to_download):
    session = requests.Session()
    for url in list_of_source_urls[:comics_to_download]:
        print("Getting: {comic_name}".format(comic_name=get_comic_name(url)))
        save_comic(session, url)


# stores the comic image on the drive in the default folder
def save_comic(session, url):
    file_name = get_comic_name(url)
    with open(os.path.join(COMICS_DIRECTORY, file_name), "wb") as comic_image:
        response = session.get(url)
        comic_image.write(response.content)


# returns a reversed list that's used to append the database of urls
def collect_new_urls(session, online_archive, difference):
    
    print("Collecting new source urls. This might take a while.")

    fresh_src_urls = []
    for url in online_archive[:difference]:
        print("Updating: {comic_name}".format(comic_name=url.split("/")[-2]))
        fresh_src_urls.append(grab_image_src_url(session, url))
    return fresh_src_urls


# updates the source url data base with fresh entries
def save_changes_to_local_datebase(list_of_new_source_urls):
    with open("data.bdkr", "a+") as data:
        for new_src_url in list_of_new_source_urls:
            data.write("{}\n".format(new_src_url))    


def download_comics_menu(comics_found):
    """
    Main download menu, takes number of available comics for download
    """
    print("\nThe scraper has found {} comics.".format(comics_found))
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


def show_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def show_summary(seconds, comics_to_download):
    print(f"Downloaded {comics_to_download} comic(s) in {show_time(seconds)}")


def perform_update(session, local_datebase, pws_archive, difference):
    if difference >= 1:
        fresh_src_urls = collect_new_urls(session, pws_archive, difference)
        local_datebase += fresh_src_urls
    else:
        print("All up-to-date. Ready player one!")

    return local_datebase[::-1]


# one function to rule them all!
def main():
    show_logo()

    session = requests.Session()

    local_datebase = upload_source_urls()
    pws_archive = check_online_archive(session)

    difference = count_difference(local_datebase, pws_archive)

    updated_database = perform_update(session, local_datebase, pws_archive, difference)

    print(updated_database[:3]) # TO-DO: Fix the download order

    comics_to_download = download_comics_menu(len(updated_database))

    start = time.time()
    create_folder()
    download_comic(updated_database, comics_to_download)
    end = time.time()

    show_summary(int(end - start), comics_to_download)
    # maintanance part
    save_changes_to_local_datebase(updated_database[:difference])
    zip_it("pwd_comics", "poorly_created_folder")
    shutil.copy2("data.bdkr", "BACKUP_data.bdkr")


if __name__ == '__main__':
    main()
