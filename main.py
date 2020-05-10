import argparse  #Para crear argumentos en el ejutable
import logging #Imprimir informacion al Usuario
logging.basicConfig(level=logging.INFO) #Nivel de informacion
import news_page_object as news
from common import config #Archivo con la configuracion de los sitios WEB

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url'] #Se obtiene la URL del sitio WEB solitado
    logging.info('IniciandoScraper para {}'.format(host))
    homepage = news.HomePage(news_site_uid,host)

    for link in homepage.article_links:
        print(link)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    new_site_choices = list(config()["news_sites"].keys()) #Obtiene lista de opciones para scraper

    parser.add_argument('news_sites', 
                        help = 'Los Sitios para scraper',
                        type= str,
                        choices=new_site_choices) #Agrega argumentos para ejecucion del usuario
    args = parser.parse_args()
    _news_scraper(args.news_sites) 