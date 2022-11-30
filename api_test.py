import requests
import json
from bs4 import BeautifulSoup

# get token from: https://api.guidedanmark.org/token

# Username = "s183898@student.dtu.dk"
# Password = "Dtu123456!"

# {{baseUrl}}/api/SearchProducts?categoryIds=79&metaTagIds=&postalCodeIds=&municipalityIds=&placeIds=&mediaChannelIds=&count=&offset=


# events -> 59

class API():
    def __init__(self):
        self.base_url = "https://api.guidedanmark.org"
        self.newest_url = None
        self.token = None
        self.max_attempts = 3
        self.token = self.get_token()
        self.categories = self.get_categories()
        self.municipalities = self.municipalities_dict()
        self.meta_tags = self.get_meta_tags()
        self.postal_codes = self.get_postal_codes()
        self.regions = self.get_regions()
        

    def get_token(self):

        req_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
        }

        req_body = {
                "grant_type": "password",
                "username": "s183898@student.dtu.dk",
                "password": "Dtu123456!"
                }

        response = requests.post(self.base_url+'/token', headers=req_header, data=req_body)

        if response.status_code == 200:
            print("Got new token")
            self.token = response.json()['access_token']
            return response.json()['access_token']
        else:
            print(response.status_code)
            print("Error updating token")
            return None
    
    def auth_header(self):
        req_header = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Authorization": f"Bearer {self.token}"
        }  
        return req_header

    def get_categories(self):
    
        req_header = self.auth_header()

        response = requests.get(self.base_url+'/api/Categories', headers=req_header)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error in request of categories:")
            print(response)
            return None
    
    def search_product(self, id = None, metaTagIds = None, postalCodeIds = None , municipalityIds = None , placeIds = None , mediaChannelIds = None, count = None, offset = None):

        req_header = self.auth_header()

        url = self.base_url + f'/api/SearchProducts?categoryIds={id}&metaTagIds={metaTagIds}&postalCodeIds={postalCodeIds}&municipalityIds={municipalityIds}&placeIds={placeIds}&mediaChannelIds={mediaChannelIds}&count={count}&offset={offset}'
        
        response = requests.get(url, headers=req_header)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error in request of product:")
            print(response)
            return None
    
    def get_meta_tags(self):

        url = self.base_url + '/api/MetaTagGroups'
        req_header = self.auth_header()

        response = requests.get(url, headers=req_header)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error in request of meta tags:")
            print(response)
            return None

    def get_product(self, id):

        req_header = self.auth_header()
        url = self.base_url + f'/api/Product/{id}'
        
        response = requests.get(url, headers=req_header)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error in request of product:")
            print(response)
            return None

    def municipalities_dict(self):
        """
        Returns a dictionary with municipality names as keys and municipality ids as values
        """

        municapals_dict = {}

        req_header = self.auth_header()
        url = self.base_url + '/api/Municipalities'
        
        response = requests.get(url, headers=req_header)

        if not response.status_code == 200:
            print("error in request of municipalities")
            print(response)
            return None

        for municapal in response.json():
            municapals_dict[municapal['Name']] = municapal['Id']
                
        return municapals_dict

    def get_postal_codes(self):
            
            req_header = self.auth_header()
            url = self.base_url + '/api/PostalCodes'
            
            response = requests.get(url, headers=req_header)
    
            if not response.status_code == 200:
                print("error in request of postal codes")
                print(response)
                return None
    
            return response.json()

    def get_regions(self):
            
            req_header = self.auth_header()
            url = self.base_url + '/api/Regions'
            
            response = requests.get(url, headers=req_header)
    
            if not response.status_code == 200:
                print("error in request of regions")
                print(response)
                return None
    
            return response.json()
    
test = API()


events = test.search_product(59, municipalityIds = test.municipalities['Middelfart'])

# get first event

event = events[1]["Descriptions"][0]["Text"]

print(event)



