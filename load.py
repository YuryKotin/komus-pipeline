import pandas as pd
import argparse
from sqlalchemy import create_engine

from schema import *


def open_new_data(date):
    data_files = [
        ('categories',    f'{categories_folder}/{date}/categories.csv'),
        ('subcategories', f'{categories_folder}/{date}/subcategories.csv'),
        ('products',      f'{products_folder}/{date}/products_full.csv'),
    ]
    db = {
        db_file[0]: {
            'df': pd.read_csv(db_file[1], index_col=0)
        }
        for db_file in data_files
    }
    db['products']['df'].drop_duplicates(subset='article', inplace=True)
    return db


def open_databases(backup=False, date=None):
    if backup and date is None:
        raise ValueError('Date is mossing for reading backuped versions')

    db_files = [
        ['categories', db_categories_file],
        ['subcategories', db_subcategories_file],
        ['dates', db_dates_file],
        ['prices', db_prices_file],
        ['products', db_products_file],
        ['descriptions', db_descriptions_file],
    ]

    if backup:
        folder = f'{bak_folder}/{date}/'
        for file in db_files:
            file[1] = folder + file[1].split('/')[-1]

    db = {
        db_file[0] : {
            'path': db_file[1],
            'df': pd.read_csv(db_file[1], index_col=0)
        }
        for db_file in db_files
    }
    return db


def save_databases(databases):
    for database in databases.values():
        database['df'].to_csv(database['path'])


def update_catalogs(db, new_data):
    db_categories = db['categories']['df']
    db_subcategories = db['subcategories']['df']

    new_categories = new_data['categories']['df']
    new_subcategories = new_data['subcategories']['df']

    updated_categories = pd.concat([db_categories, new_categories])
    updated_categories.drop_duplicates(subset=['category'], inplace=True, ignore_index=True)
    updated_categories['category_id'] = updated_categories.index + 1

    indexed_categories = updated_categories.set_index('category')
    new_subcategories['category_id'] = new_subcategories['category'].apply(
        lambda x: indexed_categories.at[x, 'category_id']
    )
    new_subcategories['subcategory_id'] = -1
    updated_subcategories = pd.concat(
        [
            db_subcategories,
            new_subcategories[['subcategory', 'subcategory_id', 'category_id', 'cat__subcat']]
        ]
    )
    updated_subcategories.drop_duplicates(subset=['subcategory', 'category_id'], inplace=True, ignore_index=True)
    updated_subcategories['subcategory_id'] = updated_subcategories.index + 1

    db['categories']['df'] = updated_categories
    db['subcategories']['df'] = updated_subcategories
    return


def update_descriptions(db, new_data):
    new_products = new_data['products']['df']
    new_descriptions = new_products[['article', 'title', 'description', 'url']]

    updated_descriptions = pd.concat([db['descriptions']['df'], new_descriptions])
    updated_descriptions.drop_duplicates(subset=['article'], inplace=True, ignore_index=True)

    db['descriptions']['df'] = updated_descriptions
    return


def update_prices(db, new_data):
    new_products = new_data['products']['df']

    dates_index = db['dates']['df'].set_index('date')
    subcategories_index = db['subcategories']['df'].set_index('cat__subcat')

    new_products['subcategory_id'] = new_products['cat__subcat'].apply(
        lambda x: subcategories_index.at[x, 'subcategory_id']
    )
    new_products['date_id'] = new_products['date'].apply(
        lambda x: dates_index.at[x, 'date_id']
    )

    updated_prices = pd.concat([
        db['prices']['df'],
        new_products[['date_id', 'article', 'price', 'discount', 'subcategory_id']]
    ])
    db['prices']['df'] = updated_prices
    return


def update_products(db, new_data):
    update_descriptions(db, new_data)
    update_prices(db, new_data)

    old_products = db['products']['df']
    new_products = new_data['products']['df']

    new_products['first_subcategory'] = new_products['subcategory_id']
    new_products['first_seen'] = new_products['date_id']
    new_products['last_seen'] = new_products['date_id']

    merged_df = pd.merge(
        left=old_products,
        right=new_products,
        how='outer',
        on='article',
        suffixes=('_old', '_new')
    )

    merged_df['first_subcategory'] = merged_df['first_subcategory_old'].combine_first(
        merged_df['first_subcategory_new']
    ).astype(int)

    merged_df['first_seen'] = merged_df['first_seen_old'].combine_first(
        merged_df['first_seen_new']
    ).astype(int)

    merged_df['last_seen'] = merged_df['last_seen_new'].combine_first(
        merged_df['first_seen_old']
    ).astype('int')

    db['products']['df'] = merged_df[['article', 'first_subcategory', 'first_seen', 'last_seen']]
    return


def update_dates(db, date):
    dates_df = db['dates']['df']
    if date not in dates_df['date'].values:
        year, month, day = [int(part) for part in date.split('-')]
        dates_df.loc[len(dates_df)] = [len(dates_df)+1, date, day, month, year]
    return


def uppend_postgresql_table(previous, current, table, engine):
    diff = pd.concat([previous[table]['df'], current[table]['df']], ignore_index=True)
    diff.drop_duplicates(keep=False, inplace=True)
    diff.to_sql(
        table, con=engine, index=False, if_exists='append'
    )


def update_postgresql_prices(current, engine):
    current['products']['df'].to_sql(
            'products_temp', con=engine, index=False, if_exists='replace'
    )

    sql_update = """
    UPDATE products
    SET last_seen = temp.last_seen 
    FROM products_temp AS temp
    WHERE products.article = temp.article 
        AND products.last_seen != temp.last_seen
    """
    sql_insert = """
    INSERT INTO products
    SELECT * FROM products_temp AS temp
    WHERE temp.article NOT IN (
        SELECT article FROM products
    )
    """
    sql_drop = "DROP TABLE products_temp"

    with engine.begin() as conn:
        conn.execute(sql_update)
        conn.execute(sql_insert)
        conn.execute(sql_drop)


def update_postgresql(previous, current):
    engine = create_engine('postgresql://yury:1234@localhost/komus')

    # updating categorical and date tables
    tables_first = [
        'categories',
        'subcategories',
        'dates',
    ]
    for table in tables_first:
        uppend_postgresql_table(previous, current, table, engine)

    # updating prices
    update_postgresql_prices(current, engine)

    # updating other tables
    tables_second = [
        'prices',
        'descriptions',
    ]
    for table in tables_second:
        uppend_postgresql_table(previous, current, table, engine)

    return


def pipeline(date):
    databases_curr = open_databases()
    new_data_dict = open_new_data(date)

    update_dates(databases_curr, date)
    update_catalogs(databases_curr, new_data_dict)
    update_products(databases_curr, new_data_dict)

    save_databases(databases_curr)

    databases_prev = open_databases(backup=True, date=date)
    update_postgresql(databases_prev, databases_curr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str)
    args = parser.parse_args()

    date_param = args.date.strip(' "\'')

    pipeline(date_param)
