import requests
import bs4
from common import config
import locale
from datetime import datetime

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
        article_link = self._queries['homepage_article_links']
        link_list = []
        for link in self._select(article_link['selector'], article_link['type']):
            if(link and link.has_attr('href')):
                link_list.append(link)
        return set(link['href'] for link in link_list)
    
class ArticlePage(NewsPage): #Para Extraer informacion de Page (Extencion de NewPage)
    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid,url)
        self.Time_publish = datetime
        #self.get_time()

    def get_time(self):
        article_time = self._queries['article_datepubli']
        if article_time['locale']:
            locale.setlocale(locale.LC_ALL, article_time[locale]) 

        result = self._select(article_time['selector'],article_time['type'])
        if(len(result)):

            if article_time['locale']:
                time_str_ = result[0].text.strip().strip().replace("am",'a. m.').replace('a.m.', 'a. m.').replace("AM", 'a. m.').replace("pm",'p. m.').replace('p.m.',  'p. m.').replace("PM", 'p. m.')
            else:
                time_str_ = result[0].text.strip().strip()
            self.Time_publish = datetime.strptime(time_str_, article_time["form"])
        else:
            self.Time_publish = datetime(1960)

    @property
    def body(self):
        article_body = self._queries['article_body']
        result = self._select( article_body['selector'],article_body['type'] )
        if len(result):
            text = []
            for parrafo in result:
                text.append(parrafo.get_text())
            self.get_time() #Si puede obtener el cuerpo de la noticia entonces obtiene la fecha de publicacion

            return text
        else:
            return ''

    @property
    def title(self):
        article_title = self._queries['article_title']

        result = self._select(article_title['selector'],article_title['type'])
        return result[0].text if(len(result)) else ''

    @property
    def time(self):
        return self.Time_publish.strftime("%Y_%m_%dT%H_%M_00")

