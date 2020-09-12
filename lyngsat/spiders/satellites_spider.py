import scrapy


class SatellitesSpider(scrapy.Spider):
    name = "satellites"
    start_urls = [
        'https://www.lyngsat.com/Intelsat-22.html',
        'https://www.lyngsat.com/NSS-12.html',
        'https://www.lyngsat.com/KazSat-3.html',
    ]

    def parse(self, response):
        satellite = response.url.split("/")[-1].split(".")[0]
        filename = 'data/satellite-%s.html' % satellite
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
