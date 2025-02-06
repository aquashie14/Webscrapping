'''This is a tutorial that retrieves various website links from a main website'''

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


Base_URL = 'https://reluinteractives.com/'

visited_pages = set()
def page_scrape(url,file):
    visited_pages.add(url)

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    file.write(f"URL : {url}\n")

    for link in soup.find_all('a',href=True):
        full_url = urljoin(Base_URL, link['href'])
        if full_url.startswith(Base_URL) and full_url not in visited_pages:
            page_scrape(full_url,file)

with open('webpages.txt', 'w', encoding='utf-8') as fp:
    page_scrape(Base_URL,fp)