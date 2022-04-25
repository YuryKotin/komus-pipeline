import load
from schema import *

import os
import shutil
from datetime import datetime


def create_folder(date):
    path = f'{bak_folder}/{date}'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def copy_files(bak_path):
    files_list = [
        db_categories_file,
        db_subcategories_file,
        db_prices_file,
        db_products_file,
        db_descriptions_file,
        db_dates_file,
    ]
    for file in files_list:
        shutil.copy(file, bak_path)


def pipeline(date):
    path = create_folder(date)
    copy_files(path)

    load.pipeline(date)


if __name__ == '__main__':
    # set date
    # date_param = '2022-04-01'
    # or use today
    date_param = datetime.today().strftime('%Y-%m-%d')

    pipeline(date_param)
