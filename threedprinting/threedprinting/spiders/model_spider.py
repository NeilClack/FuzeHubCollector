import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
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
                url=url,
                wait_time=20,
                screenshot=True,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        """Parses the request responses, extracts model information and sends that information to process_data() for storage."""

        # The url of the page, to be used later
        page = response.url

        # Creating soup from the response body
        soup = BeautifulSoup(response.body, "html.parser")

        # finding all print-card tags - returns a resultset
        tags = soup.find_all("print-card")

        # Iterating over the tags to get the URL and model name of each tag.
        for tag in tags:
            soup = tag
            # locate the a tag
            atag = soup.h3.a

            # Model Name
            name = atag.contents

            # Model URL
            url_slug = atag["href"]
            url = f"https://www.printables.com{url_slug}"

        # Creating filename, will use URL later
        filename = f"models-printables.html"

        # Open file and write tags.
        with open(filename, "w", encoding="utf-8") as f:
            tags = list(str(tags))
            for tag in tags:
                f.write(tag)

        self.log(f"Saved file {filename} at {datetime.now()}")
