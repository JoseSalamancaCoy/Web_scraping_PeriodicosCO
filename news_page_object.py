import requests
import bs4
from common import config

class HomePage:
    def __init__(self,news_site_uid,url):
        self._config = config()["news_sites"][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        print(url)
        self._visit(url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['typelink'],self._queries['homepage_article_links']):
            if(link and link.has_attr('href')):
                link_list.append(link)
        return set(link['href'] for link in link_list)
    
    def _select(self, type_link,query_string):
        return self._html.find_all(type_link,query_string)


    def _visit(self, url):
        requests.get("https://www.eltiempo.com")
        response = requests.get(url) #Peticion get
        response.raise_for_status() #Error ?
        self._html = bs4.BeautifulSoup(response.text, "html.parser")