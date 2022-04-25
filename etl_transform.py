import transform_catalog
import transform_data
from schema import products_folder, categories_folder

import os
from datetime import datetime


def create_folders(date):
    path = f'{categories_folder}/{date}'
    if not os.path.exists(path):
        os.makedirs(path)

    path = f'{products_folder}/{date}'
    if not os.path.exists(path):
        os.makedirs(path)


def pipeline(date):
    transform_catalog.pipeline(date)
    transform_data.pipeline(date)


if __name__ == '__main__':
    # set date
    # date_param = '2022-04-01'
    # or use today
    date_param = datetime.today().strftime('%Y-%m-%d')

    pipeline(date_param)
