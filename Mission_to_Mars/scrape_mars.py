#Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
from urllib.parse import urlsplit
import os
import pandas as pd
import time

# Function to choose the executable path to driver
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# Full Scrape function.
def scrape():

    #Mars News

    # Visit the NASA Mars News Site
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")

    #Mars Facts
    facts_url = "https://space-facts.com/mars/"

    table = pd.read_html(facts_url)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table

    #Mars Hemispheres
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
    
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.links.find_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()
        
        print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

        # Mars Data Dictionary - MongoDB """

        # Create empty dictionary for all Mars Data.
        mars_data = {}

        # Append news_title and news_paragraph to mars_data.
        mars_data['news_title'] = news_title
        mars_data['news_paragraph'] = news_paragraph

        # Append mars_facts to mars_data.
        mars_data['mars_facts'] = mars_facts

        # Append hemisphere_image_urls to mars_data.
        mars_data['hemisphere_img_path'] = hemisphere_image_urls

        print("Scrape Complete!!!")

        return mars_data