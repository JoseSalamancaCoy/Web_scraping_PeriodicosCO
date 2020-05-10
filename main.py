import argparse
import logging
logging.basicConfig(level=logging.INFO)
from common import config

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('IniciandoScraper para {}'.format(host))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    new_site_choices = list(config()["news_sites"].keys())

    parser.add_argument('news_sites',
                        help = 'Los Sitios para scraper',
                        type= str,
                        choices=new_site_choices)
    args = parser.parse_args()
    print(args.news_sites)
    _news_scraper(args.news_sites)