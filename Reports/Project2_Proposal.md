# Project 2 (Luther) Proposal

Can your marathon time be predicted?

Mailei Vargas



### Scope

Most marathon runners train for a particular goal race time.  Many of them train numerous hours over numerous weeks and even months.  Serious marathon runners train to qualify for the "holy grail" of marathons held every year in Boston, Massachusetts.  Many of those who work hard to get to Boston are "one and done".  However, there is a subset of runners called the legacy runners who consistently qualify and race it each year.  Based on previous years of Boston times and external factors (e.g. weather, age etc.), is it possible to predict a legacy runner's next race time?  Is this race time reasonable from a runner's perspective?  

### Methodology

1. Use Boston Marathon race results from 2015, 2016, 2017 as the training set. 
2. Scrape 2018 race results from the Boston Marathon site as the test set. 
3. Find/scrape weather data corresponding to each year day before race and day of race.
4. Find the legacy runners who have done all 4 races.  
5. Build a regression model relating prior years statistics to the 2018 results. 



### Data

* 2015, 2016, 2017 Boston Marathon race results is found on Kaggle [here](https://www.kaggle.com/rojour/boston-results).
* 2018 Boston Marathon races result need to be scraped from [here](http://registration.baa.org/2018/cf/Public/iframe_ResultsSearch.cfm ). 
* Scrape historical weather data for the race date of year from [here](https://www.wunderground.com/history/).



### Prediction

Race time of a legacy runner for the 2018 Boston Marathon. 



### Features

Features used for prediction:

| **Feature**       | **Type** | **Description**                                              |
| ----------------- | -------- | ------------------------------------------------------------ |
| Bib               | Numeric  | Assigned race number based on qualifying time. "F" could appear for female elites. |
| Name              | String   | Name of runner (Last, First)                                 |
| Age               | Numeric  | Age on race day (For all years)                              |
| M/F               | Category | Runner's gender                                              |
| City              | String   | Runner's city of residence                                   |
| State             | String   | Runner's state of residence (if applicable).                 |
| Country           | String   | Runner's country of residence                                |
| Citizen           | String   | Runner's nationality (optional)                              |
| 5K                | Numeric  | Runner's time at 5k (For all years)                          |
| Half              | Numeric  | Runner's time at halfway point (For all years)               |
| Official Time     | Numeric  | Runner's official finishing time (For all years)             |
| Overall           | Numeric  | Runner's overall raking (For all years)                      |
| Gender            | Numeric  | Runner's ranking in their gender (For all years)             |
| Division          | Numeric  | Runner's ranking in their age division (For all years)       |
| Weather           | Numeric  | Weather temp on day of race. (For all years)                 |
| PriorWeather      | Numeric  | Weather temp on day of race. (For all years)  (Maybe?)       |
| WeatherConditions | Category | Weather condition on day of race. (For all years)            |



### Things to consider

* Other 5K increment times available. (e.g. 10K, 15K, 20K, etc.)
* May not be enough legacy runners across all 4 years.  Consider runners that may have missed one of the years yet still have 3 total.
* Feature engineering the race times and weather data together to inform model they are related from the same year. 
* Handeling age increments every year.    