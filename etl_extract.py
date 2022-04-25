import extract_catalog
import extract_data
from schema import html_catalog_folder, html_pages_folder

import os
from datetime import datetime


def create_folders(date):
    path = f'{html_catalog_folder}/{date}'
    if not os.path.exists(path):
        os.makedirs(path)

    path = f'{html_pages_folder}/{date}'
    if not os.path.exists(path):
        os.makedirs(path)


def pipeline(date):
    create_folders(date)

    extract_catalog.pipeline(date)
    # extract_data.pipeline(date)


if __name__ == '__main__':
    # set date
    # date_param = '2022-04-01'
    # or use today
    date_param = datetime.today().strftime('%Y-%m-%d')

    pipeline(date_param)
