import scrapy
from scrapy_selenium import SeleniumRequest
from datetime import datetime


class ModelSpier(scrapy.Spider):
    """Scrapes the top 10 models from Printables.com and Thingiverse.com.
    Scrapy Spider Class
    """

    name = "models"

    def start_requests(self):
        """Makes the requests to the required websites."""
        urls = ["https://www.printables.com/model"]

        for url in urls:
            yield SeleniumRequest(
                url = url,
                wait_time = 20,
                screenshot = True,
                callback = self.parse,
                dont_filter = True
            )

    def parse(self, response):
        """Parses the request responses, extracts model information and sends that information to process_data() for storage."""

        page = response.url
        filename = f"models-printables.html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file {filename} at {datetime.now()}")
