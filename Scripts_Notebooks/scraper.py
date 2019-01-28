from bs4 import BeautifulSoup
from selenium import webdriver
import time


data_storage = {'Bib': [],
             'Name': [],
             'Age': [],
             'M/F': [],
             'City':[],
             'State': [],
             'Country': [],
             'Citizen': [],
             'Blank': [],
             '5K': [],
             '10K': [],
             '15K': [],
             '20K': [],
             'Half': [],
             '25K': [],
             '30K': [],
             '35K': [],
             '40K': [],
             'Pace': [],
             'Proj. Time': [],
             'Official Time': [],
             'Overall': [],
             'Gender': [],
             'Division': []
            }


def page_driver(url):
    '''Creates a Chrome driver and gets the html from the provided URL.
    Returns the driver and the html of the page. Particular to site:
    http://registration.baa.org/2018/cf/Public/iframe_ResultsSearch.cfm?mode=entry'''

    driver = webdriver.Chrome()
    driver.get(url)
    search_html = driver.page_source
    driver.close()
    return search_html


def search_options(options_page):
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


def scrape_results(page):
    '''This function takes the html from the page, extracts
    the table data and stores it in an external dictionary.
    '''

    soup = BeautifulSoup(page, "lxml")

    info_headers = ['Bib', 'Name', 'Age', 'M/F', 'City', 'State',
                    'Country', 'Citizen', 'Blank']

    result_headers = ['5K', '10K', '15K', '20K', 'Half', '25K',
                      '30K', '35K', '40K', 'Pace', 'Proj. Time',
                      'Official Time', 'Overall', 'Gender', 'Division']

    # scrape each participants info
    racer_info = soup.findAll("tr", {"class": "tr_header"})
    for i, racer in enumerate(racer_info):
        for key, val in zip(info_headers, racer_info[i].find_all('td')):
            data_storage[key] += [val.text.strip()]

    # scrape each participants results
    race_times = soup.findAll("table", {"class": "table_infogrid"})
    for i, time in enumerate(race_times):
        for key, val in zip(result_headers, race_times[i].find_all('td')):
            data_storage[key] += [val.text.strip()]


def scrape_by_country(countries):
    '''Scrape the race results based on the country the runner is from.'''

    url = 'http://registration.baa.org/2018/cf/Public/iframe_ResultsSearch.cfm'
    driver = webdriver.Chrome()
    driver.get(url)
    max_limit = 1000

    for country in countries:

        if country == 'United States of America' or country == 'Canada':
            continue

        country_option = driver.find_element_by_name("CountryOfResID")
        country_option.send_keys(country)

        limit = driver.find_element_by_name("VarTargetCount")
        limit.send_keys(max_limit)

        try:
            xpath1 = '//*[@id="PublicSearch"]/div/div/input'
            submit_button = driver.find_elements_by_xpath(xpath1)[0]
            time.sleep(3)
            submit_button.click()
            scrape_results(driver.page_source)
        except IndexError:
            xpath4 = '/html/body/div/div/div/div/table[2]/tbody/tr/td[1]/form/input'
            search_again = driver.find_elements_by_xpath(xpath4)[0]
            time.sleep(3)
            search_again.click()
            continue

        try:
            xpath2 = ('/html/body/div/div/div/div/table[4]/tbody/tr/td/'
                      'table/tbody/tr[51]/td/table/tbody/tr/td[2]/form/input[2]')
            next_button = driver.find_elements_by_xpath(xpath2)[0]
            time.sleep(3)
            next_button.click()
            scrape_results(driver.page_source)
        except IndexError:
            xpath4 = '/html/body/div/div/div/div/table[2]/tbody/tr/td[1]/form/input'
            search_again = driver.find_elements_by_xpath(xpath4)[0]
            time.sleep(3)
            search_again.click()
            continue

        xpath3 = ('/html/body/div/div/div/div/table[3]/tbody/tr/td/table/tbody'
                  '/tr[51]/td/table/tbody/tr/td[2]/form/input[2]')
        while True:
            try:
                next_button = driver.find_elements_by_xpath(xpath3)[0]
                time.sleep(3)
                next_button.click()
                scrape_results(driver.page_source)
            except IndexError:
                xpath4 = '/html/body/div/div/div/div/table[2]/tbody/tr/td[1]/form/input'
                search_again = driver.find_elements_by_xpath(xpath4)[0]
                time.sleep(3)
                search_again.click()
                break


def scrape_by_state(states, divisions):
    '''Scrape the race results based on the state runner is from.'''

    url = 'http://registration.baa.org/2018/cf/Public/iframe_ResultsSearch.cfm'
    driver = webdriver.Chrome()
    driver.get(url)
    max_limit = 1000

    for state in states:
        for division in divisions:
            # populate the provided drop down fields
            division_option = driver.find_element_by_name("AwardsDivisionID")
            division_option.send_keys(division)
            state_option = driver.find_element_by_name("StateID")
            state_option.send_keys(state)
            limit = driver.find_element_by_name("VarTargetCount")
            limit.send_keys(max_limit)

            try:
                xpath1 = '//*[@id="PublicSearch"]/div/div/input'
                submit_button = driver.find_elements_by_xpath(xpath1)[0]
                time.sleep(3)
                submit_button.click()
                scrape_results(driver.page_source)
            except IndexError:
                xpath4 = '/html/body/div/div/div/div/table[2]/tbody/tr/td[1]/form/input'
                search_again = driver.find_elements_by_xpath(xpath4)[0]
                time.sleep(3)
                search_again.click()
                continue

            try:
                xpath2 = ('/html/body/div/div/div/div/table[4]/tbody/tr/td/'
                          'table/tbody/tr[51]/td/table/tbody/tr/td[2]/form/input[2]')
                next_button = driver.find_elements_by_xpath(xpath2)[0]
                time.sleep(3)
                next_button.click()
                scrape_results(driver.page_source)
            except IndexError:
                xpath4 = '/html/body/div/div/div/div/table[2]/tbody/tr/td[1]/form/input'
                search_again = driver.find_elements_by_xpath(xpath4)[0]
                time.sleep(3)
                search_again.click()
                continue

            xpath3 = ('/html/body/div/div/div/div/table[3]/tbody/tr/td/table/tbody'
                      '/tr[51]/td/table/tbody/tr/td[2]/form/input[2]')
            while True:
                try:
                    next_button = driver.find_elements_by_xpath(xpath3)[0]
                    time.sleep(3)
                    next_button.click()
                    scrape_results(driver.page_source)
                except IndexError:
                    xpath4 = '/html/body/div/div/div/div/table[2]/tbody/tr/td[1]/form/input'
                    search_again = driver.find_elements_by_xpath(xpath4)[0]
                    time.sleep(3)
                    search_again.click()
                    break
