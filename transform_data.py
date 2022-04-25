import glob
import pandas as pd
import argparse
from tqdm import tqdm
import os.path

from schema import products_folder, html_pages_folder
from parse_data import PageData, select_css


def get_category_from_path(path):
    file_name = path.split('/')[-1]
    category_name = '__'.join(
        file_name.split('__')[:-1]
    )
    return category_name


def parse_concat_data(date):
    items = []
    files = glob.glob(f'{html_pages_folder}/{date}/*')

    with open(files[0], 'r') as file:
        html = file.read()
    try:
        css = select_css(html)
    except ValueError:
        raise ValueError(f'error on {files[0]}')

    for file_path in tqdm(files):
        with open(file_path, 'r') as file:
            html = file.read()

        item_entries = PageData(html, css).item_entries

        cat__subcat = get_category_from_path(file_path)
        for item in item_entries:
            item['cat__subcat'] = cat__subcat
            item['date'] = date

        items.extend(item_entries)

    return items


def get_prices(full_df):
    prices_df = pd.DataFrame(
        full_df[['article', 'price', 'discount', 'cat__subcat', 'date']]
    )
    return prices_df


def get_descriptions(full_df):
    descriptions_df = pd.DataFrame(
        full_df[['article', 'title', 'description', 'url']]
    )
    return descriptions_df


def pipeline(date):
    products_full_path = f'{products_folder}/{date}/products_full.csv'
    if not os.path.isfile(products_full_path):
        products_full = pd.DataFrame(
            parse_concat_data(date)
        )
        products_full.to_csv(products_full_path)
    else:
        products_full = pd.read_csv(products_full_path, index_col=0)

    prices = get_prices(products_full)
    descriptions = get_descriptions(products_full)

    prices.to_csv(f'{products_folder}/{date}/prices.csv')
    descriptions.to_csv(f'{products_folder}/{date}/descriptions.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)
    args = parser.parse_args()

    date_param = args.date.strip(' "\'')

    pipeline(date_param)
    pass
