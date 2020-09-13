import scrapy

from lyngsat.items import Frequency, Provider, Frequencies


def _get_frequency_data(column):
    url = ""
    if "<a" in column:
        url = scrapy.Selector(text=column).css('a').attrib['href']

    freq_data = scrapy.Selector(text=column).css('font').getall()
    beam = ""
    eirp = ""
    frequency = ""
    if len(freq_data) == 3:
        frequency = scrapy.Selector(text=freq_data[0]).xpath("//text()").get().replace(u'\xa0', u' ')
        #beam = scrapy.Selector(text=freq_data[1]).xpath("//text()").get()
        eirp = scrapy.Selector(text=freq_data[2]).xpath("//text()").get()
    if len(freq_data) == 4:
        frequency = scrapy.Selector(text=freq_data[1]).xpath("//text()").get().replace(u'\xa0', u' ')
        beam = scrapy.Selector(text=freq_data[2]).xpath("//text()").get()
        eirp = scrapy.Selector(text=freq_data[3]).xpath("//text()").get()

    return Frequency(frequency=frequency, url=url, beam=beam, eirp=eirp)


def _get_provider_data(logo_column, provider_column, system_column, sr_fec_column, onidtd_column, source_updated_column):
    logo_url = None
    provider_url = None
    provider_name = None
    if "(feeds)" not in provider_column:
        if "img" in logo_column:
            logo_url = scrapy.Selector(text=logo_column).css('img').attrib['src']
        if "<a" in provider_column:
            provider_url = scrapy.Selector(text=provider_column).css('a').attrib['href']
            provider_name = scrapy.Selector(text=provider_column).css('a').xpath("//text()").get()
    system = scrapy.Selector(text=system_column).xpath("/font/font//text()").get()
    #TODO
    return Provider(provider=provider_name, url=provider_url, logo_url=logo_url, system=system)


class SatellitesSpider(scrapy.Spider):
    name = "satellites"
    start_urls = [
        'https://www.lyngsat.com/Intelsat-22.html',
        # 'https://www.lyngsat.com/NSS-12.html',
        # 'https://www.lyngsat.com/KazSat-3.html',
    ]

    def parse(self, response):
        satellite = response.url.split("/")[-1].split(".")[0]
        filename = 'data/satellite-%s.html' % satellite

        tables = response.css("table.bigtable").xpath("//table[@width='720']").getall()
        frequencies = []
        for table in tables[3:-2]:
            rows = scrapy.Selector(text=table).xpath("//tr").getall()
            if len(rows) >= 4 and "News at" not in table:
                previous_frequency = None
                previous_provider = None
                for row in rows[2:-1]:
                    columns = scrapy.Selector(text=row).xpath("//td").getall()
                    if "salmon" in columns[0]:
                        frequency = _get_frequency_data(columns[1])
                        previous_frequency = frequency
                        frequencies.append(frequency)
                        if len(columns) == 9:
                            provider = _get_provider_data(columns[2], columns[3], columns[5], columns[6], columns[7],
                                                          columns[8])
                            previous_provider = provider
                        else:
                            previous_provider = None
                        frequencies.append(frequency)

        yield Frequencies(frequencies=frequencies)
