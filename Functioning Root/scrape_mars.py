from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    time.sleep(1)

def scrape_info():
    browser = init_browser()

    # Visit Nasa Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    
    # Get the news Title and News Teaser
    news_title = soup.find_all('div', class_="content_title")[1].text
    news_p = soup.find('div', class_="article_teaser_body").text

    # Visit JPL for images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)

    # Navigate to Location for Image
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    # Find link to image
    image_link = browser.find_link_by_partial_text('.jpg')

    # Assign image url to variable
    jpl_img_url = image_link['href']

    # Visit Mars Weather Twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    
    # Get the latest Mars Weather
    mars_weather =  soup.find('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text

    # Mars Facts Table Scraping
    url = 'https://space-facts.com/mars/'

    # Read all HTML tables with Pandas
    mars_tables = pd.read_html(url)

    # Select Correct table for DataFrame
    mars_info_df = mars_tables[0]

    # Rename Columns and set index
    mars_info_df.columns = ['', 'Value']
    mars_info_df.set_index('', inplace=True)

    # Convert DataFrame to HTML string and remove line breaks
    mars_info_html = mars_info_df.to_html()
    mars_info_html = mars_info_html.replace('\n', '')
    
    # Gather Hemisphere Photos
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(7)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    
    # Find Hemisphere Titles and compile into a list
    hemi_titles = soup.find_all('h3')
    hemi_list = []
    for title in hemi_titles:
        hemi_list.append(title.text)

    # Navigate to each page gathering all necessary urls
    url_list = []
    for hemi in hemi_list:
        browser.click_link_by_partial_text(hemi)
        time.sleep(1)
        image = browser.find_link_by_partial_text('Sample')
        image_url = image['href']
        url_list.append(image_url)
        browser.back()
        time.sleep(1)
    
    #Initialize Hemi url list
    hemi_img_urls = []

    # Append Hemisphere Title and Image URL as dictionaries to url list
    url_len = len(url_list)
    for x in range(0, url_len):
        hemi_img_urls.append({"title":hemi_list[x], "img_url":url_list[x]})

    # Define Dictionary to be uploaded
    mars_data = {'news_title': news_title,
                'news_p': news_p,
                'jpl_img_url':jpl_img_url,
                'mars_weather': mars_weather,
                'mars_info_html': mars_info_html,
                'hemi_img_title_1': hemi_img_urls[0]['title'],
                'hemi_img_url_1': hemi_img_urls[0]['img_url'],
                'hemi_img_title_2': hemi_img_urls[1]['title'],
                'hemi_img_url_2': hemi_img_urls[1]['img_url'],
                'hemi_img_title_3': hemi_img_urls[2]['title'],
                'hemi_img_url_3': hemi_img_urls[2]['img_url'],
                'hemi_img_title_4': hemi_img_urls[3]['title'],
                'hemi_img_url_4': hemi_img_urls[3]['img_url'],
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data