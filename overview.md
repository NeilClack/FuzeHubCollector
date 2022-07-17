# Fuze Hub Collector
This documentation needs to be removed as it covers the entire project and not one single piece of it. - To be completed later.

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
 


---  
---  
---  

#### Notes for Later  
##### Database  
- I had to create the database and table + columns and constraints manually. This isn't a big deal because it only needs to be done once, but an auto-setup script would be nice.   