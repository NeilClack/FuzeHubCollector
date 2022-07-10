import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class PrintablesSpier(scrapy.Spider):
    """Scrapes the top 10 models from Printables.com and Thingiverse.com.
    Scrapy Spider Class
    """

    name = "printables"

    def start_requests(self, url: str = None):
        """Makes the requests to the required websites."""

        if url is None:
            urls = ["https://www.printables.com/model"]
        else:
            urls = url

        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                screenshot=True,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        """Parses the request responses, extracts model information and sends that information to process_data() for storage."""

        # Creating soup from the response body
        soup = BeautifulSoup(response.body, "html.parser")


        # Creating an empty dataframe.
        columns = ["name", "likes", "slug", "url", "image_url"]
        df = pd.DataFrame(columns=columns)

        for tag in soup.find_all("print-card"):
            soup = tag
            model = {
                "name": soup.h3.a.contents[0].strip(),
                "likes": int(soup.find("app-like-print").span.contents[0]),
                "slug": soup.h3.a["href"],
                "url": f"https://www.printables.com{soup.h3.a['href']}",
                "image_url": f"https://www.printables.com{soup.find('print-card-image').picture.source['srcset']}",
                "datetime": datetime.now()
            }

            df = pd.concat([df, pd.DataFrame([model])], ignore_index=True)

        df = df.sort_values(by=["likes"], ascending=False)
        df.to_csv('pandas_test.csv', index=False)