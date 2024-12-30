import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib3

#ignore the errors
urllib3.disable_warnings()

class Link:
    def __init__(self,url,session):
        self.url = url
        self.session = session

        
    def extract_urls(self):
        r = self.session.get(self.url,verify=False)
        soup = BeautifulSoup(r.text,'lxml')
        links = []
        links.append(self.url)
        for link in soup.findAll('a'):
            #link =  '<a href="https://sgs.edu.in/parent-zone-overview/">Parent Zone  Overview</a>'
            try:
                link = url_parser(link.get('href'),self.url)
                if link != None:
                    links.append(link)
            except:
                pass

        return links



#parse and verify all the urls
def url_parser(url,baseURL):
    #if netloc there
    if urlparse(url).netloc:
        #then check if its same
        if urlparse(url).netloc == urlparse(baseURL).netloc:
            return url
        else:
            pass
    #if not there , internal url
    else:
        return (urlparse(baseURL).scheme + '://' + urlparse(baseURL).netloc + '/' + url)
    