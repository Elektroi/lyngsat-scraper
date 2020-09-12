#Lyngsat scraper

This scraper obtains the information from the web https://www.lyngsat.com and saves it in different files in csv format.

##Prerequisites
You need to have installed the python [![scrapy](https://scrapy.org/)] library.

##Run
There are two spiders, one to obtain the satellites of each continent, and another to obtain the information of each satellite (in process)

### Continents
Executing this command `scrapy crawl continents` save in a csv the different satellites that exist per continent.

