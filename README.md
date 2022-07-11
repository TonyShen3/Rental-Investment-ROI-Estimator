# Rental-Investment-ROI-Estimator
Python program that scrapes Airbnb listings, rents, and housing prices to calculate projected ROI on rental investments
<br />
File Descriptions:
<ul>
  <li><b> Main.py </b> - main code that scrapes web for housing price and Airbnb rates, then storing them in a SQLite3 database </li>
  <li><b> ROIEstimnator.py </b> - script that scrapes web for housing price and Airbnb rates based on user inputs, run in local python environment </li>
  <li><b> ScraperFunction.py </b> - contains scraper functions for scraping housing price, Airbnb rates and mortgage rate  </li>
  <ul>
    <li>Caution: large scale scraping may violate website's Term of Service. Please verify the website you scrape from allows for large scale scraping before use </li>
  </ul>
  <li><b> MajorUSCities,py </b> - contains major U.S. zip codes ranked by population  </li>
  <li><b> ROIdata.db </b> - scraped SQLite3 database example  </li>
  <li><b> MapGenerator.py </b> - generate html web app to display scraped data using Folium  </li>
  <li><b> ROIMap.html </b> - web app result </li>
</ul>
 
