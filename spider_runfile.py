from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from fuze_hub_collector.spiders.models import PrintablesSpider


process = CrawlerProcess(get_project_settings())
process.crawl(PrintablesSpider)
process.start()
