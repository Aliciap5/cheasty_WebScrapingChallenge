from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import pymongo
from selenium import webdriver



def scrape():
    driver = webdriver.Chrome()

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&blank_scope=Latest'
    driver.get(url)
    soup = bs4(driver.page_source, 'html.parser')
    try:
        news_title = soup.find_all(class_="content_title")[1].text
    except:
        news_title = []
    try:
        news_desc = soup.find_all(class_="article_teaser_body")[0].text
    except:
        news_desc = []
    
    # Visit the url for JPL Featured Space Image here.
    url2 ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    driver.get(url2)
    soup2 = bs4(driver.page_source, 'html.parser')  

    featured_image_url = soup2.find('article', class_="carousel_item")['style']
    featured_image_url = featured_image_url.replace("background-image: url('","").replace("');","")

    image_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
    url3 ='https://twitter.com/marswxreport?lang=en'
    response3 = requests.get(url3)
    soup3 = bs4(response3.text, 'html.parser')

    mars_weather = soup3.find(class_="tweet").text

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url4 ='https://space-facts.com/mars/'
    data = pd.read_html(url4)
    df= data[0]
    df.columns=['Measurment','Data']
    html = df.to_html()
    



    url5 ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response5 = requests.get(url5)
    soup5 = bs4(response5.text, 'html.parser')

    hemispheres = soup5.find_all(class_="item")
    titles = []
    urls = []
    for hemi in hemispheres:
        name = hemi.find('h3').text
        src = hemi.find('img')['src']        
        src= f"https://astrogeology.usgs.gov{src}"
        titles.append(name)
        urls.append(src)

            
    mars_data = {"news_title": news_title
        , "news_desc": news_desc
        , "image_url": image_url
        , "mars_weather": mars_weather
        , "html":html
        , "titles": titles
        , "urls": urls}

    driver.quit()
    return mars_data