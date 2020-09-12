import csv
import scrapy

from lyngsat.model.satellite import Satellite
from lyngsat.spiders.satellites_spider import SatellitesSpider


class ContinetsSpider(scrapy.Spider):
    name = "continents"

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is not None:
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            urls = [
                'https://www.lyngsat.com/asia.html',
                'https://www.lyngsat.com/europe.html',
                'https://www.lyngsat.com/atlantic.html',
                'https://www.lyngsat.com/america.html',
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        continent = response.url.split("/")[-1].split(".")[0]
        filename = 'data/continent-%s.csv' % continent

        table = response.css("table.bigtable").xpath("//table[@align='center']").get()
        rows = scrapy.Selector(text=table).xpath("//tr").getall()

        satellites = []
        previous_grade = ""
        for row in rows:
            line = scrapy.Selector(text=row).xpath("//td").getall()

            if len(line) == 5 or len(line) == 4:
                index = 0;
                if len(line) == 5:
                    grade = "".join(scrapy.Selector(text=line[1]).xpath("//text()").getall())
                    previous_grade = grade
                    index = 1
                url =  "https://www.lyngsat.com/"+scrapy.Selector(text=line[1]).css('a').attrib['href']
                name = "".join(scrapy.Selector(text=line[index+1]).xpath("//text()").getall())
                band = "".join(scrapy.Selector(text=line[index+2]).xpath("//text()").getall()).strip()
                date = "".join(scrapy.Selector(text=line[index+3]).xpath("//text()").getall())
                grade = previous_grade

                sat = Satellite(continent=continent, url=url, grade=grade, name=name, band=band,
                                date=date)
                satellites.append(sat)
            #else:
            #    print("Don't parsed line: " + "".join(line))

        with open("data/"+continent+".csv", 'w+') as csv_file:
            wr = csv.writer(csv_file, delimiter=';')
            for item in satellites:
                wr.writerow(list(item))
        self.log('Saved file %s' % filename)
