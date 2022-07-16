import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
import re


def save_models(df: pd.DataFrame = None) -> None:
    """Sorts the provided DataFrame of scraped models and saves or updates the top 10"""
    models = df.sort_values(by=["likes"], ascending=False).head(10).to_dict("records")
    # Creating the db engine
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/fuzehubdb", future=True
    )

    models_table = Table("models", MetaData(), autoload_with=engine)

    with engine.connect() as conn:
        for model in models:
            insert_stmt = (
                insert(models_table)
                .values(
                    model_id=model["model_id"],
                    name=model["name"],
                    likes=model["likes"],
                    slug=model["slug"],
                    uri=model["uri"],
                    image_uri=model["image_uri"],
                    last_update=model["last_update"],
                )
                .on_conflict_do_update(index_elements=["model_id"], set_=model)
            )
            conn.execute(insert_stmt)
            conn.commit()


class PrintablesSpider(scrapy.Spider):
    """Scrapes the top liked models in the last 7 days from Printables.com,
    sorts the resulting models,
    then stores them in the database
    """

    name = "printables"

    def start_requests(self):
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
        columns = ["name", "likes", "slug", "uri", "image_uri", "last_update"]
        df = pd.DataFrame(columns=columns)

        for tag in soup.find_all("print-card"):
            soup = tag
            model = {
                "model_id": int(
                    re.findall("[^model/][0-9]+[^-...]", soup.h3.a["href"])[0]
                ),
                "name": soup.h3.a.contents[0].strip(),
                "likes": int(soup.find("app-like-print").span.contents[0]),
                "slug": soup.h3.a["href"],
                "uri": f"https://www.printables.com{soup.h3.a['href']}",
                "image_uri": f"{soup.find('print-card-image').picture.source['srcset']}",
                "last_update": datetime.utcnow(),
            }

            df = pd.concat([df, pd.DataFrame([model])], ignore_index=True)

        save_models(df)


class ThingiverseSpider(scrapy.Spider):
    """Scrapes the top liked models in the last 7 days from Thingiverse.com,
    sorts the resulting models,
    then stores them in the database
    """

    name = "thingiverse"

    def start_requests(self):
        """Makes the requests to the required websites."""

        urls = ["https://www.thingiverse.com"]

        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                screenshot=True,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        pass
