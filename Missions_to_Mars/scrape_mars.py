import requests as rq, pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser 

def scrape():

    # Web Scraping Homework - Mission to Mars#
    executable_path = {"executable_path": r"chromedriver.exe"}
    browser = Browser('chrome', headless=False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    listofdicts = []
    mars_data = {}

                #1 

    # Get all content titles 
    news_title_soup = soup.find('div', class_='content_title').text
    news_p_soup = soup.find("div", class_ ="article_teaser_body").text

    news_title = {'title':news_title_soup}
    news_p=  {'title':news_p_soup}

    mars_data['title'] =  news_title_soup
    mars_data['news_p'] = news_p_soup
    
    
                #2

    # JPL Mars Space Images - Featured Image
    executable_path = {"executable_path": r"chromedriver.exe"}
    browser = Browser('chrome', headless=False)
    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Featured image link
    baseurl = "https://www.jpl.nasa.gov"
    featured_image_url = soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    mars_data['featured_img_url'] = featured_image_url
   
                #3

    # Mars Weather last tweet
    executable_path = {"executable_path": r"chromedriver.exe"}
    browser = Browser('chrome', headless=False)
    url= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
   
    # weather tweet text
    mars_weather = soup.find('div',class_="js-tweet-text-container").text
 
    mars_data['mars_weather'] = mars_weather[9:-27]
    
            #4

    ### Mars Facts table
    executable_path = {"executable_path": r"chromedriver.exe"}
    browser = Browser('chrome', headless=False)
    url= 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # Scrape the table containing facts with pandas (multiple tables inside)
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts_df = tables[1]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df.set_index("Description", inplace=True)
    # Use Pandas to convert the data to a HTML table string.
    mars_facts = mars_facts_df.to_html()
 

    mars_data['mars_facts'] = mars_facts
    
    # Visit the USGS Astrogeology site
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url="https://astrogeology.usgs.gov"


    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    main_url = soup.find_all('div', class_='item')

    titles=[]
    list_titles= []
    list_dictionaries= []
    dictionary ={}
    onelist = []
    hemisphere_image_urls= []
    for x in main_url:
        title = x.find('h3').text
        list_titles.append(title)
        scrapped_pic_url = x.find('a')['href']
        img_url= base_url+scrapped_pic_url
        browser.visit(img_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_parent = soup.find('div',class_='downloads')
        img_url = img_parent.find('a')['href']
        
        dictionary= {'title':title, 'img_url':img_url }
        list_dictionaries.append(dictionary)


    
    mars_data['hemisphere_image_urls'] = list_dictionaries
    
    
    return mars_data