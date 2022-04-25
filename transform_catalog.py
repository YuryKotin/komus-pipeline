import pandas as pd
import argparse

from schema import html_catalog_folder, categories_folder


def read_data(date):
    path = f'{html_catalog_folder}/{date}/Продукты питания.csv'
    return pd.read_csv(path, index_col=0)


def get_categories(data):
    categories = pd.DataFrame(
        data['category'].unique()
    ).rename(columns={0: 'category'})
    return categories


def get_subcategories(data):
    subcategories = pd.DataFrame(
        data[['category', 'subcategory']]
    )
    subcategories['cat__subcat'] = subcategories['category'] + '__' + subcategories['subcategory']
    return subcategories


def save_data(cats, subcats, date):
    cats.to_csv(f'{categories_folder}/{date}/categories.csv')
    subcats.to_csv(f'{categories_folder}/{date}/subcategories.csv')


def pipeline(date):
    data = read_data(date)
    categories = get_categories(data)
    subcategories = get_subcategories(data)
    save_data(categories, subcategories, date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)
    args = parser.parse_args()

    date_param = args.date.strip(' "\'')

    pipeline(date_param)
