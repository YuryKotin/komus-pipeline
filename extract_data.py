import requests
import glob
import time
from tqdm import tqdm
import argparse
from contextlib import redirect_stdout
import pandas as pd

from headers import headers
from schema import html_catalog_folder, html_pages_folder


def open_catalog(date):
    path = f'{html_catalog_folder}/{date}/Продукты питания.csv'
    return pd.read_csv(path)


def form_download_list(catalog_data):
    download_list = []
    for item in catalog_data.itertuples():
        category    = item.category
        subcategory = item.subcategory
        link        = item.link
        n_pages     = item.n_pages

        for page in range(n_pages):
            file_name = f'{category}__{subcategory}__{page}.html'
            url = f'https://www.komus.ru{link}?from=footer_menu&listingMode=PLAIN&page={page}'

            download_list.append(
                [file_name, url]
            )

    return download_list


def download_pages(download_list, date, sleep=10):
    folder = f'{html_pages_folder}/{date}'
    already_downloaded_pages = set(glob.glob(f'{folder}/*'))
    for item in tqdm(download_list):
        file_name, url = item
        file_path = f'{folder}/{file_name}'
        if file_path in already_downloaded_pages:
            continue

        response = requests.get(url, headers=headers)
        html = response.content

        with open(file_path, 'wb') as file:
            with redirect_stdout(file):
                file.write(html)

        time.sleep(sleep)


def pipeline(date):
    catalog_data = open_catalog(date)
    download_list = form_download_list(catalog_data)
    download_pages(download_list, date, sleep=5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)

    args = parser.parse_args()

    date_param = args.date.strip(' "\'')

    pipeline(date_param)
