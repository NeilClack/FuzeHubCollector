# 3D-Printing-Trends-Dashboard
A simple dashboard for tracking 3D printing model trends and material prices 

---  
## Table of Contents
  * [Business Problem](#business-problem)
  * [Data](#data-sources-storage-and-organization)
  * [Tech Stack](#tech-stack)
  * [Deployment](#deployment)
  * [Insights](#insights)
  * [Results](#results) 

---  
## Business Problem  

I run a small 3D printing business. In my experience, it's a good idea to supplement custom print income by selling pre-printed designs. I have a hard time keeping up with trends and what prints are currently popular so I decided to collect, analyze and visualize this data into an easily digestible online dashboard. I also need to know what brands of filament cost at any given time since I use specific brands for different materials. This helps me keep track of which materials to use, where to buy them from and keep costs down to a minimum.  

---  
## Data Sources, Storage and Organization  

I have scraped this data from several sources on the web. Printable models were scraped from Thingiverse's most recent top 10, as well as Printables.com most liked top 10 mmodels. Filament stock and prices was pulled from several online 3D printing stores and websites from local stores near me. All data is currently saved in a sqlite database on my server. All scraped data is stored in a time series fashion. Pricing information is kept for up to 3 months, and popular models only for about 45 days. Some models, such as those seen for the entirety of those 45 days, are archived as "superstar designs" and can be referenced at any time.  

--- 
## Tech Stack  
* Python 3.10  
    * Scrapy  
    * Pandas  
* SQLite3  
* Ubuntu  
* Heroku  

---  
## Deployment  

_COMING SOON_

---  
## Insights  

_COMING SOON_

---  
## Results  

_COMING SOON_

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
