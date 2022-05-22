# import dependancies
import pandas as pd
from splinter import Browser
import time
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # set up splinter
    browser = Browser('chrome',executable_path=ChromeDriverManager().install(),headless=False)
    # visit Red Planet science site url using splinter
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)
    time.sleep(1)
    # set the variablesand scrape into soup
    html = browser.html
    soup = bs(html,"html.parser")
    # set variable for title and get one
    news_title = soup.find('div', class_= 'content_title').get_text()
    # news_title
    news_p = soup.find('div', class_= 'article_teaser_body').get_text()
    # news_p
    # visit Space images site url using splinter
    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)
    # find full sized image and click
    full_image = browser.find_by_tag('button')[1]
    full_image.click()
    # set the variables and scrape into soup
    html = browser.html
    img_soup = bs(html,"html.parser")
    # find the relative url
    rel_img_url = img_soup.find('img', class_='fancybox-image').get('src')
    # rel_img_url
    # create the absolute url and save to variable called featured_image_url
    featured_image_url = f'https://spaceimages-mars.com/{rel_img_url}'
    #featured_image_url
    
    df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    #df.head()
    # rename columns and set index
    df.columns=['Feature','Mars','Earth']
    df.set_index('Feature', inplace=True)
    #df
    # convert the data to a HTML table string
    html_table = df.to_html()
    # Visit the marshemispheres site to obtain high-resolution images for each hemisphere of Mars.
    url3 = 'https://marshemispheres.com/'
    browser.visit(url3)
    #set variables again for new URL
    html = browser.html
    soup = bs(html, 'html.parser')
    # create an empty list to store a dictionary of image titles and image urls and save to a variable called hemisphere_image_urls
    hemisphere_image_urls = []
    # create list to image urls
    abs_url_list = []
    #find all div tags with class description and iterate over them
    for div in soup.findAll("div", attrs={"class":"description"}):
        #find all hyperlinks
        rel_url_list = div.findAll("a")
        #iterate over hyperlinks
        for link in rel_url_list:
            #get the url
            href = link['href']
            #turn url into full url
            abs_url = url3+ href
            #append url to list
            abs_url_list.append(abs_url)

    #print url list to check
    #print(abs_url_list)
    #print(rel_url_list)
    for link in abs_url_list:
        url = link
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
            #find all divs with class downloads
        for div in soup.findAll("div", attrs={"class": "downloads"}):
            base_url = "https://marshemispheres.com/"
            #find links with text Original and take href
            img_url = base_url + div.find("a", text="Sample")["href"]
            #find h2 and get text from h2
            h2 = soup.find("h2").get_text()
            # remove word Enhanced
            title = h2.replace("Enhanced","")
            #remove whitespace at end
            title = title.rstrip()
            #create dictionary to hold results
            title_img_dict = {
            "title": title,
            "img_url": img_url
            }
            #append dictionary to list of dictionaries
            hemisphere_image_urls.append(title_img_dict)
    #check list of dictionaries
    #print(hemisphere_image_urls)            
    #close the splinter browser
    browser.quit()

    scrape_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "table": html_table,
        "image_urls": hemisphere_image_urls
    }

    return(scrape_data)
  







