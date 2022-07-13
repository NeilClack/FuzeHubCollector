from email.generator import Generator
import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3

class PrintablesSpier(scrapy.Spider):
    """Scrapes the top liked models in the last 7 days from Printables.com, 
    sorts the resulting models, 
    then stores them in the database
    """

    name = "printables"

    def start_requests(self, url: str = None) -> Generator:
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

    def parse(self, response) -> pd.DataFrame:
        """Parses the response object and returns a dataframe of model information."""

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
                "last_update": datetime.now(),
            }

            df = pd.concat([df, pd.DataFrame([model])], ignore_index=True)

        self.save(df=df)


    def save(self, df: pd.DataFrame=None) -> None:
        """Sorts and then saves dataframe to database."""

        # Create connection to db
        conn = sqlite3.connect('printables.db')

        # Sort models by likes
        df = df.sort_values(by=['likes'], ascending=False)

        # Filter to to 10
        df = df.head(10)

        # Validation
        print(df.head(10))

        # Update database
        df.to_sql("models", con=conn, if_exists="replace")
