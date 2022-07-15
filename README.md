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
    * SQLAlchemy  
* PostgreSQL ( *for local development only )  
* Ubuntu  
* AWS  
  * Lambda
  * Aurora SQL

---  
## Deployment  

1. Install Python dependencies  
2. Install google-chrome-stable  
3. Verify google-chrome version  
4. Download matching chromedriver  
5. Unzip driver and place in fuze_hub_collector directory  
6. Run

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


### Testing Scrapy  
#### Problem:  
  - Scrapy includes a testing framework called "contracts", and while contracts may work, my concern is that making these requests takes time, and I'm currently working with a very, very slow internet connection. What I want to do is somehow save the content of the scrape and then run tests against that saved content rather than making new requests each time. This means I won't be wasting time waiting for my connection to, well, connect, the page to load, and scrapy to receive the response.  

#### Solution:  
  - Betamax! Betamax makes a request and stores the resulting content into a file called a "cassette", which can be replayed over and over again. I'll only need to make the request once, and if something breaks during a test, I can delete the cassette and Betamax will go out and make a new request to the site to grab the most up to date content. This way it's easier to determine if a bug is being caused by a website update or by a code issue. This is much easier than manually loading the site, then saving the page to html and placing it in the correct location, all of this work is done for me.

### Managing the Scraped Models  
#### Problem:  
  - While I can now scrape today's models, I want to do a few very specific things with them before they get stored in the database. First, I want to compare my current list of models to the newly scraped list of models. This will be followed up with one of two functions. 1. Move the model to "archived" if it does not appear on the newly scraped model list. 2. Keep the model but update the like count and keep the original scraped date. This allows me to do a few things. I'll be able to track and archive models that fall off the popular list, and I can also track models that stay on the list for extended periods of time without adding any outside data such as a counter or anything like that. It's worth noting that if someone updates the title of their model, I currently will be comparing titles and the model will become duplicated, but, I can worry about this later.  

#### Solution:  
  - I will create a static field in the database table called "date_added", which will, by default, use the datetime stamp of the record insertion. When inserting records, they will not include this field which means the field will always default to "now", updates will also not touch this field and the update method will be an "upsert", so insert unless exists then update. 

  This greatly simplifies this entire process, and, allows for more analysis points further in the future such as like history and trend marking if a model resurfaces on the trending list. 
