import argparse  #Para crear argumentos en el ejutable
from datetime import datetime
import csv
import logging #Imprimir informacion al Usuario
import re
import numpy as np
import pandas as pd

from requests.exceptions import HTTPError,TooManyRedirects
from urllib3.exceptions import MaxRetryError
logging.basicConfig(level=logging.INFO) #Nivel de informacion
import news_page_object as news
from common import config #Archivo con la configuracion de los sitios WEB


logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$') #http://Periodico.com/loquesea
is_root_path = re.compile(r'^/.+$') # /Loquesea

def _news_scraper(news_site_uid, Time):
    host = config()['news_sites'][news_site_uid]['url'] #Se obtiene la URL del sitio WEB solitado
    _time = datetime.strptime(Time,"%Y/%m/%d")
    
    articles = []
    #        URL : [Ya se visito para extraer links, Esta al interior de la revista, Tiene contenido]
    links = pd.DataFrame(columns=["getlinks","inPage", "getCont", "url"]) 
    links.loc[len(links)] = [False,True,False,host]

    while not links.getlinks.all(): #Verifica si hay paginas por obtener links
        for link_scraper in links[ links.getlinks == False ]["url"]:
            logging.info('***************************************************************\n\n\n\n\n\n\n\n\n')
            logging.info('IniciandoScraper para {}'.format(link_scraper))
            homepage = news.HomePage(news_site_uid,link_scraper) #Inicializa pagina principal


            for link in homepage.article_links: #Obtiene y recorre links
                article = _fetch_article(news_site_uid,host,link,_time) #Valida el nuevo articulo en base al contenido y la fecha de publicacion
                
                url= _build_link(host,link)
                if len(links[links.url == url]): #Si ya existe no agrega link a tabla
                    pass
                else:
                    
                    links.loc[len(links)] = [False,Check_host(host,url), False, url]

                if article:
                    logger.info("Articulo Valido")
                    articles.append(article)
                    
                    links.getCont[links.url == link_scraper] = True
                    break

            links.getlinks[links.url == link_scraper] = True
    Save_links(news_site_uid,links)
    _save_articles(news_site_uid,articles)

def Check_host(host,url):
    if host == url[:len(host)]:
        return True
    else:
        return False
def Save_links(news_site_uid,links):
    out_file_name = '../DataSet/{}_links.csv'.format(news_site_uid)
    links.to_csv(out_file_name)
def _save_articles(news_site_uid,articles):
    now = datetime.now().strftime('%Y_%m_%d')
    out_file_name = '../DataSet/{}_{}_articles.csv'.format(news_site_uid,now)
    csv_headers = list(filter(lambda property: not property.startswith('_'),dir(articles[0])))
    #Se le pasa las posibles ejecuciones de la funcion arg (article)
    with open(out_file_name, mode = 'w+', encoding="utf-8") as f:
        writer = csv.writer(f,delimiter='¬')
        writer.writerow(csv_headers)
        for article in articles:
            row = [str(getattr(article,prop)) for prop in csv_headers]
            writer.writerow(row)

def _fetch_article(news_site_uid,host,link,_time):
    logger.info('Revisando {}'.format(link))
    article = None
    try:
        article = news.ArticlePage(news_site_uid,_build_link(host,link))
    except (HTTPError, MaxRetryError,TooManyRedirects) as e:
        logger.warning('Error cuando check el articulo', exc_info= False)

    if(article) and (not article.body or article.Time_publish < _time) :
        #logger.warning("Articulo invalido")
        return None
    
    return article

def _build_link(host,link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host,link)
    else:
        return '{host}/{url}'.format(host=host, url=link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    new_site_choices = list(config()["news_sites"].keys()) #Obtiene lista de opciones para scraper

    parser.add_argument('news_sites', 
                        help = 'Los Sitios para scraper',
                        type= str,
                        choices=new_site_choices) #Agrega argumentos para ejecucion del usuario
    
    parser.add_argument('Time', 
                        help = 'Fecha desde la que se desea scraper. Ej: 2020/05/01',
                        type= str) #Agrega argumentos para ejecucion del usuario
    args = parser.parse_args()
    _news_scraper(args.news_sites,args.Time) 