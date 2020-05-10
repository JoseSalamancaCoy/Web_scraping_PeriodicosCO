import requests
import bs4
from common import config
from multipledispatch import dispatch #Multiples Definiciones
from functools import singledispatch

class NewsPage: #Obtiene html de pagina
    def __init__(self,news_site_uid,url):
        self._config = config()["news_sites"][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self.url = url
        self._visit(url)

    def _select(self, query_string, type_link = None):
        if not type_link:
            return self._html.select(query_string)
        else:
            return self._html.find_all(type_link,class_=query_string)
    
    def _visit(self, url):
        response = requests.get(url) #Peticion get
        response.raise_for_status() #Error ?
        self._html = bs4.BeautifulSoup(response.text, "html.parser")

class HomePage(NewsPage): #Para Obtener links de Page (Extencion de NewPage)
    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid,url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links'], self._queries['typelink']):
            if(link and link.has_attr('href')):
                link_list.append(link)
        return set(link['href'] for link in link_list)
    
class ArticlePage(NewsPage): #Para Extraer informacion de Page (Extencion de NewPage)
    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid,url)

    @property
    def body(self):
        result = self._select( self._queries['article_body'],"p" )
        if len(result):
            text = []
            for parrafo in result:
                text.append(parrafo.get_text())
            return text
        else:
            return ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'],'h1')
        return result[0].text if(len(result)) else ''

    @property
    def fecha(self):
        result = self._select(self._queries['article_datepubli'])
        return result[0].text.replace('\n','') if(len(result)) else ''
        
    #@property
    #def link(self):
    #    return self.url
