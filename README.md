# pws_remastered

~~~

                                                   _               _ 
  a comical web-scraper                           | |             | |
  _ ____      _____   _ __ ___ _ __ ___   __ _ ___| |_ ___ _ __ __| |
 | '_ \ \ /\ / / __| | '__/ _ \ '_ ` _ \ / _` / __| __/ _ \ '__/ _` |
 | |_) \ V  V /\__ \ | | |  __/ | | | | | (_| \__ \ ||  __/ | | (_| |
 | .__/ \_/\_/ |___/ |_|  \___|_| |_| |_|\__,_|___/\__\___|_|  \__,_|
 | |             ______                                              
 |_|            |______|                   version: alpha | June 2019 

~~~
A fresh take on poorlydrwanlines.com comic image scraper based on my previous [script](https://github.com/baduker/poorlywrittenscraper).

There are some major changes and improvements over the first edition.

**What's new?**

[![hotshit.png](http://www.poorlydrawnlines.com/wp-content/uploads/2019/06/hot-shit-kevin.png)](http://www.poorlydrawnlines.com/comic/hot-shit/)

1. The script come swith a pre-loaded list of source urls to speed up scraping.
2. There's going to be a simple .json file based database of comic names, comic urls, source image urls, dates (published & downloaded), and comic number. -> **TO BE IMPLEMENTED**
3. The scraping algorithm has been updated.
4. A new, colorful logo is going to great you. **TO BE IMPLEMENTED**
5. A built-in zip feature for easier sharing of downloaded comics.

**Road map**

An overview of what's been done so far.

- [x] DONE! :collision:
- [ ] TO-DO :shit:

- [x] A list of all source urls has been collected and saved to a list.
- [x] Implemented a method that compares the local list with the online source and updates the local database with new urls.
- [x] The scraping algorithm has been updated to match the changes in the source website HTML code.
- [x] There's a buil-in zip method that compresses the comic download folder.