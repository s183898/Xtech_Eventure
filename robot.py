import urllib3

class Scraper:
    def __init__(self, input_url):
        self.input_url = input_url
        self.url = self.root_url()
        self.links = []

    def get_html(self, url):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        return r.data.decode('utf-8')

    def get_links(self, url):
        links = []
        html = self.get_html(url)
        html = html.split('\n')

        for line in html:
            if '<a href=' in line:
                link = line.split('"')[1]
                if link not in links:
                    links.append(link)
        
        return links
    
    def get_robot_txt(self):
        robot_url = self.url + '/robots.txt'
        http = urllib3.PoolManager()
        r = http.request('GET', robot_url)
        return r.data.decode('utf-8')

    def root_url(self):
        root_url = self.input_url.split('//')[1]
        root_url = root_url.split('/')[0]
        return root_url        

zarpaulo = Scraper('https://www.zarpaulo.com/dfsfdsf')

url = zarpaulo.url

links = zarpaulo.get_links(url)

for link in links:
    print(zarpaulo.get_links(url+"/"+link))

lydmor = Scraper("https://www.lydmor.dk/")

url = lydmor.url

links = lydmor.get_links(url)

print(links)
print()
print(lydmor.get_robot_txt())
