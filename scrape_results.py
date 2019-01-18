# import pandas as pd
# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# import time




def open_page(url):
    '''Creates a Chrome driver and gets the html from the provided URL.
    Returns the driver and the html of the page'''

    # url = 'http://registration.baa.org/2018/cf/Public/iframe_ResultsSearch.cfm'
    driver = webdriver.Chrome()
    return driver.get(url), driver.page_source


def scrape_options(options_page):
    '''Takes html from Boston Marthon search page and parse it for the search options'''

    soup = BeautifulSoup(options_page, "lxml")

    divisions = []
    gender = []
    states = []
    countries = []

    list_names = [divisions, gender, states, countries]
    select_names = ['AwardsDivisionID', 'GenderID', 'StateID', 'CountryOfResID']

    for lst, name in zip(list_names, select_names):
        options = soup.find('select', {'name': name})
        for option in options.findAll('option'):
            if option.text.strip() != '':
                lst.append(option.text.strip())

    return divisions, gender, states, countries



