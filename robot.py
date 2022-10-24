import urllib3
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, input_url):
        self.input_url = input_url
        self.url = self.root_url()
        self.links = []

    def get_html(self, url):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        return r.data.decode("unicode_escape")

    def get_links(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for line in soup.find_all('a'):
            link = line.get('href')
            if link != "" and link != "#" and link != None:
                if self.url in link and link != url:
                    links.append(link)
                if "https://" not in link:
                    links.append("https://"+self.url + link)
        return links

    def get_robot_txt(self):
        robot_url = self.url + '/robots.txt'
        return self.get_html(robot_url)

    def root_url(self):
        root_url = self.input_url.split('//')[1]
        root_url = root_url.split('/')[0]
        return root_url

    def search_keyword(self, keyword, text):
        if keyword in text:
            return True
        else:
            return False

if __name__ == "__main__":
    link = 'https://lydmor.dk'
    scraper = Scraper(link)
    links = scraper.get_links(link)
    print(links)
