# pws_remastered

~~~
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
        version: 0.1.3
~~~

This is a remake of one of my first ever non-trivial Python 
[scripts](https://github.com/baduker/poorlywrittenscraper) for a popular comic
page [poorlydrwanlines.com](http://poorlydrawnlines.com).

I've decided to give it another shot because I feel like I've learned a thing
or two over the past year and the initial script lacks in certain areas. 

[![learn.png](http://www.poorlydrawnlines.com/wp-content/uploads/2019/06/learn.png)](http://www.poorlydrawnlines.com/comic/learn/)

Here's a list of some the major changes and improvements over the first edition.

**What's new?**

1. The script comes with a pre-loaded JSON to speed up scraping but also allows
to narrow down the scraping scope to e.g. a year and/or a month and gives a nice
little peek into the statistics (Still to be implemented) 
2. The scraping algorithm has been updated and now supports LXML and XPath.
3. A new, colorful logo is there to great you each time you launch the script.
Long live the ASCII art!

**Requirements**

- [x] Python 3.6+
- [x] requests
- [x] colorama
- [x] lxml

Create a new virtual environment with Python 3.6+ and then just type:
> pip3 install -r requirements.txt

**The dump**

As of July 2019, the entire dump of comics can be found
[here](https://yadi.sk/d/3KO2w_sfJxU8Tg).
