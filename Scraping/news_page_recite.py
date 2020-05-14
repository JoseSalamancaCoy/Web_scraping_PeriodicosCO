import argparse
import logging
logging.basicConfig(level= logging.INFO)

from urllib.parse import urlparse

import pandas as pd

logger = logging.getLogger(__name__)

def main(filename):
    logger.info('Comensando proceso de limpieza')

    df = _read_data(filename)
    newspaper_iud = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df,newspaper_iud)
    df = _extract_host(df)

    return df

def _read_data(filename):
    logger.info('Leyendo archivo {}'.format(filename))

    return pd.read_csv(filename,error_bad_lines=False, sep= "¬",delimiter=None, header='infer')

def _extract_newspaper_uid(filename):
    logger.info('Extrayendo newspaper uid')
    newspaper_iud = filename.split('_')[0]

    logger.info('Newspaper uid detectado: {}'.format(newspaper_iud))
    return newspaper_iud

def _add_newspaper_uid_column(df, newspaper_iud):
    logger.info('Se llena columna con newspaper columna con {}'.format(newspaper_iud))
    df['newspaper_uid'] = newspaper_iud

    return df

def _extract_host(df):
    logger.info('Extrayendo host de url')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('filename',
                    help= 'El pad del directorio de datos',
                    type = str)

    args = parse.parse_args()

    df = main(args.filename)
    print(df)