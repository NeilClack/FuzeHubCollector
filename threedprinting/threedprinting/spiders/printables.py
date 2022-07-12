from email.generator import Generator
import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3

class PrintablesSpier(scrapy.Spider):
    """Scrapes the top liked models in the last 7 days from Printables.com
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
                "datetime": datetime.now()
            }

            df = pd.concat([df, pd.DataFrame([model])], ignore_index=True)

        self.save(df=df)


    def save(self, df: pd.DataFrame=None) -> None:
        """Sorts and then saves dataframe to database."""

        # Read existing table
        # Compare existing table with new results
        # If model exists in existing table and new results
            # update like count only*
        # If model exists in existing table and not new results
            # archive model
        # If model does not exist in table but exists in new results
            # add model
        # * This allows for the least amount of database writes, while keeping the original datetime
        # and thus allowing the function of tracking long-term trending items. 


        # Read existing table

        # Compare existing table (df) to new table (ndf)
        
            # Add objects to drop to tdf

        # Write ndf to table

        # Archive tdf objects and drop from models table

        conn = sqlite3.connect('printables.db')

        df = df.sort_values(by=['likes'], ascending=False)
        df.to_sql("models", con=conn, if_exists="replace")
