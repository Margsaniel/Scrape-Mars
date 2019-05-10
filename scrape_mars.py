# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser


def scrape():
#latest news    
    marsinfo_url = 'https://mars.nasa.gov/news'
    response = requests.get(marsinfo_url)

    soup = BeautifulSoup(response.text, 'html5lib')

    marstitle = soup.find('div', class_= 'content_title').text
    marspar = soup.find('div', class_='rollover_description_inner').text.strip('\n\r\t": ')

#space image
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    imageurl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(imageurl)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    mars_image = browser.find_by_tag("figure").first.find_by_tag("a")["href"]


#Mars Twitter Info
    mars_twitter = requests.get("https://twitter.com/marswxreport?lang=en")
    mars_twittersoup = BeautifulSoup(mars_twitter.text, 'html.parser')
    
    mars_twitterreport = mars_twittersoup.find_all('div', class_="js-tweet-text-container")
    
    mars_weather = mars_twitterreport[0].text

#Facts
    mars_facts = requests.get("https://space-facts.com/mars/")
    mars_space_facts =  pd.read_html(mars_facts.text)
    
    table = mars_space_facts[0]
    table.set_index(0, inplace =True)
    mars_table = table
    facts_html = mars_table.to_html()
    
#Archeologywebsites - hemispheres images
    images = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    images = requests.get(images)
    soup = BeautifulSoup(images.text, "html.parser")
    
    images_links = soup.find_all('div', class_='item')
    images_url = 'https://astrogeology.usgs.gov'
    
    hemisphere_urls = []
    for img in images_links:
        img_title = img.find('h3').text
        img_url = img.find('a', class_='itemLink product-item')['href']
        browser.visit(images_url + img_url)
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        fullimg_url = images_url + soup.find('img', class_='wide-image')['src']
        hemisphere_urls.append({"title" : img_title, "img_url" : fullimg_url})
        
    mars_data = {
        "News_Title": marstitle,
        "Paragraph_Text": marspar,
        "Most_Recent_Mars_Image": mars_image,
        "Mars_Weather": mars_weather,
        "mars_h": hemisphere_urls
     }

    return mars_data