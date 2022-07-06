import scrapy
from datetime import datetime

class ModelSpier(scrapy.Spider):
    name = 'models'

    def start_requests(self):
        url = 'https://www.printables.com/model'
        
        yield(scrapy.Request(url=url, callback=self.parse))

    def parse(self, response):
        page = response.url
        filename = f'models-printables'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename} at {datetime.now()}')