import argparse  #Para crear argumentos en el ejutable
from datetime import datetime
import csv
import logging #Imprimir informacion al Usuario
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
logging.basicConfig(level=logging.INFO) #Nivel de informacion
import news_page_object as news
from common import config #Archivo con la configuracion de los sitios WEB


logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$') #http://Periodico.com/loquesea
is_root_path = re.compile(r'^/.+$') # /Loquesea

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url'] #Se obtiene la URL del sitio WEB solitado
    logging.info('IniciandoScraper para {}'.format(host))
    homepage = news.HomePage(news_site_uid,host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid,host,link)

        if article:
            logger.info("Articulo Valido")
            articles.append(article)
    _save_articles(news_site_uid,articles)

def _save_articles(news_site_uid,articles):
    now = datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{}_{}_articles.csv'.format(news_site_uid,now)
    csv_headers = list(filter(lambda property: not property.startswith('_'),dir(articles[0])))
    #Se le pasa las posibles ejecuciones de la funcion arg (article)
    with open(out_file_name, mode = 'w+') as f:
        writer = csv.writer(f,delimiter='¬')
        writer.writerow(csv_headers)
        for article in articles:
            row = [str(getattr(article,prop)) for prop in csv_headers]
            writer.writerow(row)
def _fetch_article(news_site_uid,host,link):
    logger.info('Revisando {}'.format(link))

    article = None
    try:
        article = news.ArticlePage(news_site_uid,_build_link(host,link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error cuando check el articulo', exc_info= False)

    if(article) and not article.body:
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
    args = parser.parse_args()
    _news_scraper(args.news_sites) 