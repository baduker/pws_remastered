# pws_remastered

~~~
                                                   _               _ 
  a comical web-scraper                           | |             | |
  _ ____      _____   _ __ ___ _ __ ___   __ _ ___| |_ ___ _ __ __| |
 | '_ \ \ /\ / / __| | '__/ _ \ '_ ` _ \ / _` / __| __/ _ \ '__/ _` |
 | |_) \ V  V /\__ \ | | |  __/ | | | | | (_| \__ \ ||  __/ | | (_| |
 | .__/ \_/\_/ |___/ |_|  \___|_| |_| |_|\__,_|___/\__\___|_|  \__,_|
 | |             ______                                              
 |_|            |______|                                 version: 1.0

~~~
A fresh take on [poorlydrwanlines.com](http://poorlydrawnlines.com) comic image scraper based on my previous [script](https://github.com/baduker/poorlywrittenscraper).

There are some major changes and improvements over the first edition.

**What's new?**

[![hotshit.png](http://www.poorlydrawnlines.com/wp-content/uploads/2019/06/learn.png)](http://www.poorlydrawnlines.com/comic/learn/)

1. The script comes with a pre-loaded list of source urls to speed up scraping. 
2. The scraping algorithm has been updated.
3. A new, colorful logo is there to great you each time you launch the script.
4. A built-in zip feature for easier sharing of downloaded comics.
5. There's going to be a simple .json file based database of comic names, comic urls, source image urls, dates (published & downloaded), and comic number. -> **TO BE IMPLEMENTED**

**The dump**

As of July 2019, the entire dump of comics can be found [here](https://yadi.sk/d/3KO2w_sfJxU8Tg).

**Road map**

An overview of what's been done so far.

- [x] DONE! :collision:

- [x] Add a list of all source urls.
- [x] Implement a method that compares the local list with the on-line source and updates the local database with new urls.
- [x] update the scraping algorithm to match the changes in the source website HTML code.
- [x] Add a built-in zip method that compresses the comic download folder.
- [x] Implement a colorful logo.
- [x] Implement a method to back up the local database of source urls.