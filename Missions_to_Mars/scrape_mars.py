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

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)

    # standard copy/pasta for my html / soup
    html = browser.html
    img_bs = BeautifulSoup(html, 'html.parser')

    featured_img = img_bs.find("img",class_="headerimage fade-in").get('src')
    listings["final_img_url"] = f'{img_url}{featured_img}'

    return listings