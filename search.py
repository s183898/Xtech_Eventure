import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

from robot import Scraper

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

def google_search(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://translate.google')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

searches = google_search("events near me")

for search in searches[:2]:
    scraper = Scraper(search)
    html = scraper.pretty_html(scraper.get_html(search))

    print(html)
