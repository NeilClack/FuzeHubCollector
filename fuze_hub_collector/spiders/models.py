from psycopg2 import OperationalError, ProgrammingError
import logging
import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
import sys
import re


def save_models(df: pd.DataFrame = None) -> None:
    """Sorts the provided DataFrame of scraped models and saves or updates the top 10"""
    models = df.sort_values(by=["likes"], ascending=False).head(10).to_dict("records")

    try:
        # Creating the db engine
        engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/fuzehubdb",
            future=True,
        )
    except OperationalError as e:
        logging.error(e)

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

            try:
                conn.execute(insert_stmt)
            except ProgrammingError as e:
                logging.error("e %s", (insert_stmt))
            except:
                logging.error(sys.exc_info)

            try:
                conn.commit()
            except:
                raise


class PrintablesSpider(scrapy.Spider):
    """Scrapes the top liked models in the last 7 days from Printables.com,
    sorts the resulting models,
    then stores them in the database
    """

    # name for scrapy to call when crawling
    name = "printables"

    # Logging configuration
    logging.basicConfig(
        filename=f"{name}.log",
        format="%(levelname)s: %(asctime)s - %(message)s",
        level=logging.ERROR,
    )

    def start_requests(self):
        """Makes the requests to the required websites."""

        urls = ["https://www.printables.com/model"]

        for url in urls:
            logging.info(f"Requesting {url}...")
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                screenshot=True,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response) -> pd.DataFrame:
        """Parses the response object and returns a dataframe of model information."""

        try:
            # Creating soup from the response body
            soup = BeautifulSoup(response.body, "html.parser")
        except:
            logging.error("Error creating soup from resulting webpage.")
            logging.error(exc_info)

        # Creating an empty dataframe.
        columns = ["name", "likes", "slug", "uri", "image_uri", "last_update"]
        df = pd.DataFrame(columns=columns)

        for tag in soup.find_all("print-card"):
            soup = tag
            try:
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
            except:
                logging.error("Error in creating model dictionary.")
                logging.error(sys.exc_info)

            df = pd.concat([df, pd.DataFrame([model])], ignore_index=True)

        save_models(df)
