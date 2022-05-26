# Import dependencies
# ----------------------------------------
import pandas as pd
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.firefox import GeckoDriverManager
# ----------------------------------------


# Initialize scraping
# ----------------------------------------
def scrapeAll():
  # Set up splinter
  executable_path = {'executable_path': GeckoDriverManager().install()}
  browser = Browser('firefox', **executable_path, headless=False)

  news_title, news_paragraph = marsNews(browser)

  # Run all scraping functions and store results in dict
  data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featuredImage(browser),
    "facts": marsFacts(),
    "last_modified": dt.datetime.now()
  }

  # Stop websriver and return data
  browser.quit()
  return data
# ----------------------------------------


# Red Planet News Title and Paragraph
# ----------------------------------------
def marsNews(browser):
  # Visit the mars nasa news site
  url = 'https://redplanetscience.com'
  browser.visit(url)

  # Optional delay for loading the page
  browser.is_element_not_present_by_css('div.list_text', wait_time=1)

  # Set up html parser
  html = browser.html
  news_soup = soup(html, 'html.parser')

  try:
    slide_elem = news_soup.select_one('div.list_text')
    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    # User the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
  except AttributeError:
    return None, None

  return news_title, news_p
# ----------------------------------------


# ## JPL Space Images Featured Image
# ----------------------------------------
def featuredImage(browser):
  # Visit URL
  url = 'https://spaceimages-mars.com'
  browser.visit(url)

  # Find and click the full image button
  full_image_elem = browser.find_by_tag('button')[1]
  full_image_elem.click()

  # Parse the resulting html with soup
  html = browser.html
  img_soup = soup(html, 'html.parser')

  try:
    # Find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
  except AttributeError:
    return None

  # Use the base url to create an absolute url
  img_url = f'https://spaceimages-mars.com/{img_url_rel}'

  return img_url
# ----------------------------------------


# Mars Facts
# ----------------------------------------
def marsFacts():
  try:
    # Grab first table of webpage and create DF from it
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
  except BaseException:
    return None

  # Assign columns and set description as index
  df.columns=['Description', 'Mars', 'Earth']
  df.set_index('Description', inplace=True)

  # Convert DF to html-ready code
  return df.to_html(classes="table table-striped")
# ----------------------------------------


# Main method
# ----------------------------------------
if __name__ == "__main__":
  # If running as script, print scraped data
  print(scrapeAll())
# ----------------------------------------
