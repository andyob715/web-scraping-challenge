from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

# Setup splinter

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=True) 
    return browser

def scrape():
    browser = init_browser()
    listings = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    listings["news"] = soup.find_all('div', 'content_title')[1].get_text()
    listings["teasers"] = soup.find_all('div', 'article_teaser_body')[1].get_text()

    #new url for image scraping
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)

    # standard copy/pasta for my html / soup
    html = browser.html
    img_bs = BeautifulSoup(html, 'html.parser')

    featured_img = img_bs.find("img",class_="headerimage fade-in").get('src')
    listings["final_img_url"] = f'{img_url}{featured_img}'

    #new url for facts scraping
    mars_facts_url='https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    facts_keys = []
    facts_values = []
    facts_final = {}

    # standard copy/pasta for my html / soup
    html = browser.html
    facts_bs = BeautifulSoup(html, 'html.parser')

    mars_facts_table = facts_bs.find("table",class_="tablepress-id-p-mars")
    mars_facts_table_1 = mars_facts_table.find_all("td", class_="column-1")
    for i in range(len(mars_facts_table_1)):
        facts_keys.append(mars_facts_table_1[i].text)
    mars_facts_table_2= mars_facts_table.find_all("td", class_="column-2")
    for i in range(len(mars_facts_table_2)):
        facts_values.append(mars_facts_table_2[i].text)

    for i in range(len(facts_keys)):
        facts_final[facts_keys[i]] = facts_values[i]
    
    listings["facts_table"] = facts_final

    return listings