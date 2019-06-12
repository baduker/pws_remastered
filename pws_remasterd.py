#!/usr/bin/python3

"""
A simple image downloader for poorlydrawnlines.com/archive
"""
import os
import time
import sys


import requests


DEFAULT_DIR_NAME = "poorly_created_folder"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)


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
def load_data():
    with open("data.bdkr", "r") as data:
      source_urls = data.readlines()
    return [line[:-1] for line in source_urls]


# creates a default download folder
def create_folder():
  os.makedirs(DEFAULT_DIR_NAME, exist_ok=True)


# chops off the tail of source url to get a comic name
def get_comic_name(url):
  return url.split("/")[-1]


# fetches the comic image from the comic server
def download_comic(list_of_source_urls):
  create_folder()
  session = requests.Session()
  pbar_counter = 1
  for url in list_of_source_urls:
    print("Getting: {comic_name}".format(comic_name=get_comic_name(url)))
    save_comic(session, url)
    pbar_counter += 1


# stores the comic image on the drive in the default folder
def save_comic(session, url):
  file_name = get_comic_name(url)
  with open(os.path.join(COMICS_DIRECTORY, file_name), "wb") as comic_image:
    response = session.get(url)
    comic_image.write(response.content)


# one functions to rule them all!
def main():
  show_logo()
  download_comic(load_data()[:5])


if __name__ == '__main__':
  main()