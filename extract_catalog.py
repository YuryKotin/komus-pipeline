import requests
import argparse
from contextlib import redirect_stdout
import pandas as pd
import os.path

from headers import headers
from parse_catalog import Catalog
from schema import html_catalog_folder


def catalog_already_loaded(path):
    return os.path.isfile(f'{path}/Продукты питания.html')


def load_catalog():
    url = 'https://www.komus.ru/katalog/produkty-pitaniya/c/1028/?from=footer_menu'
    response = requests.get(url, headers=headers)
    return response.content


def save_catalog(html, path):
    with open(f'{path}/Продукты питания.html', 'wb') as file:
        with redirect_stdout(file):
            file.write(html)


def parse_catalog(html):
    return Catalog(html).data


def save_data(data, path):
    pd.DataFrame(data).to_csv(f'{path}/Продукты питания.csv')


def pipeline(date):
    # raise ValueError('Html schema of catalog page has been changed and not properly parsed yet')
    
    path = f'{html_catalog_folder}/{date}'
    if not catalog_already_loaded(path):
        html = load_catalog()
        save_catalog(html=html, path=path)
    else:
        with open(f'{path}/Продукты питания.html', 'rb') as file:
            html = file.read()
    df = parse_catalog(html)
    save_data(df, path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default='')
    args = parser.parse_args()

    catalog_date = args.date

    pipeline(catalog_date)
