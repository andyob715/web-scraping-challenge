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

    # Hemis scrape portion
    hemis_url = 'https://marshemispheres.com/'
    browser.visit(hemis_url)

    # standard copy/pasta for my html / soup
    html = browser.html
    hemis_bs = BeautifulSoup(html, 'html.parser')

    hemi_keys = []
    hemi_values = []
    dupes = []
    img_source_list = []
    hemi_dict_final = {}

    #use the find all for the title and teaser
    hemi1 = hemis_bs.find_all('h3')
    for i in range(len(hemi1)-1):
        hemi_keys.append(hemi1[i].text)
        
    hemi2 = hemis_bs.find_all("a", class_="itemLink product-item")
    for i in range(len(hemi2)-1):
        hemi_img = hemi2[i].get("href")
        final_url = f'{hemis_url}{hemi_img}'
        if final_url in hemi_values:
            dupes.append(final_url)
        else:
            hemi_values.append(final_url)

    for i in range(len(hemi_values)):
        url = f'{hemi_values[i]}'
        browser.visit(url)

        # standard copy/pasta for my html / soup
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        #use the find all for the title and teaser
        full_img = soup.find('img', class_="wide-image").get('src')
        full_img_url = f'https://astrogeology.usgs.gov/cache/{full_img}'
        img_source_list.append(full_img_url)
        
    #create a dictionary of the final values
    for i in range(len(hemi_keys)):
        hemi_dict_final[hemi_keys[i]] = img_source_list[i]
        
    listings["hemispheres_name"] = hemi_keys
    listings["hemispheres_img"] = img_source_list
    
    return listings