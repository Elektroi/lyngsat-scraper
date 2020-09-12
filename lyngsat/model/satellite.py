class Satellite(object):

    def __init__(self, continent, name, grade, url, band, date):
        self.continent = continent
        self.name = name
        self.grade = grade
        self.url = url
        self.band = band
        self.date = date

    def __iter__(self):
        return iter([self.continent, self.name, self.grade,  self.url, self.band, self.date])
