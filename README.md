# Fuze Hub Collector  
Web scraping utility for Fuze Hub  
--- 

## Table of Contents  
- [About This](#about-this)  
- [Deployment](#deployment)  
- [Development Roadmap](#development-roadmap)  
- [Changelog](#changelog)  
- [Challenges](#challenges)  
---  
## About This  

---  
## Deployment  

_This app is deployed via Docker container within AWS Lambda, storing data on an AWS Aurora - Postgres instance._  


---  
## Development Roadmap  


---  
## Changelog  

---  
## Challenges  

### Rendering Javascript
#### Problem:  
  - scrapy cannot execute Javascript. The sites I want to scrape 3D models from require rendering model lists in Javascript. 
#### Solution:  
  - I had to come up with a way to render Javascript in a headless server environment, quickly, and without switching scraping platforms. I could use Selenium to directly scrape these websites, however in past experiences, Selenium scraping is much slower than Scrapy, plus Scrapy makes it incredibly fast and easy to setup a new scraper, or, "spider". I did some digging and discoverd three possible solutions:  

    1. Scrapy-Selenium: A Scrapy middleware that utilizes Selenium to run Chrome or Firefox headless browsers to render the Javascript.  
    2. Scrapy-Splash: Another Scrapy middleware, built by the Scrapy team. It's been around for a while but requires coding in Lua to interact with websites and only uses a custom headless browser.  
    3. ScrapingBee: A web scraping API utilizing a headless Chrome browser. At a glance, it appears to operate the same way for Scrapy that Dask does for Pandas, by taking the place of the Scrapy code to do the hard work for you. This looks like the easiest option to setup and use, but has a steep price of $49/mo for their cheapest option.  

    This leaves me with but one choice, Scrapy-Selenium!

### Parsing the Results  
#### Problem:  
  - Scrapy includes an HTML parser directly, however I personally have found it to be cumbersome and sometimes unintuitive in it's selection clauses. This has prompted me to try a different approach this time.  

#### Solution:  
  - I decided, for now, to utilize BeautifulSoup 4 (or, BS4). It parses the HTML pretty well and when it does so, gives direct methods to call to select specific tags, which will be helpful in the case of Printables.com since they created their own tag to represent a "model card" called <print-card> so we should end up with something similar to soup.find_all('print-card') to get all of these items. Of course, this might change later but for now this solution makes the most sense and appears to be the least amount of effort.

### Managing the Scraped Models  
#### Problem:  
  - Storing the models in a database proved to be quite a challenge. I needed to save new models as they appeared, remove old models as they dropped off the top 10, and also update any existing models without outright rewriting them so that I could keep the original date added. 
  In Postgres, insertion and updating can be done with what is known as an upsert. I needed to implement this in the save_models function.

#### Solution:  
  - I decided not to remove the old models as they dropped off the list. Instead, I added the "date_added" and a "last_updated" column so that I can track a models original insertion date, the last time it was updated, and these together can tell me how long a model has been trending as well as if a model is _still_ trending without having to remove anything from the database, opening the doors to historical model tracking. Instead, on the frontend, I will only render the top 10 sorted by likes and filtered by last_update datetime with a span of the last 7 days. 
