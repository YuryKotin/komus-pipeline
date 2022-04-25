from schema import *

import pandas as pd


# def append_missing_prices(df_prices, df_products):
#     first_price = pd.merge(left=df_products, right=df_prices,
#                            left_on=['article', 'first_seen'],
#                            right_on=['article', 'date_id'],
#                            how='left')
#     first_price.set_index('article', inplace=True)
#
#     last_price = pd.merge(left=df_products, right=df_prices,
#                           left_on=['article', 'last_seen'],
#                           right_on=['article', 'date_id'],
#                           how='left')
#     last_price.set_index('article', inplace=True)
#
#     update_entries = []
#     min_date_id = df_prices['date_id'].min()
#     max_date_id = df_prices['date_id'].max()
#     for entry in df_products.itertuples():
#         if entry.first_seen > min_date_id:
#             update_entries.extend(
#                 [
#                     {
#                         'date_id': date_id,
#                         'article': entry.article,
#                         'price': first_price.loc[entry.article, 'price'],
#                     }
#                     for date_id in range(1, entry.first_seen)
#                 ]
#             )
#     for entry in df_products.itertuples():
#         if entry.last_seen < max_date_id:
#             update_entries.extend(
#                 [
#                     {
#                         'date_id': date_id,
#                         'article': entry.article,
#                         'price': last_price.loc[entry.article, 'price'],
#                     }
#                     for date_id in range(entry.last_seen+1, max_date_id+1)
#                 ]
#             )
#     return pd.DataFrame(update_entries)


if __name__ == '__main__':
    categories = pd.read_csv(db_categories_file, index_col=0)
    subcategories = pd.read_csv(db_subcategories_file, index_col=0)
    dates = pd.read_csv(db_dates_file, index_col=0)
    prices = pd.read_csv(db_prices_file, index_col=0)
    products = pd.read_csv(db_products_file, index_col=0)
    descriptions = pd.read_csv(db_descriptions_file, index_col=0)

    prices.drop(columns='subcategory_id', inplace=True)

    # append_prices = append_missing_prices(prices, products)
    # prices = pd.concat(
    #     [
    #         prices,
    #         append_prices
    #      ]
    # )

    analysis_categories = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]
    categories = categories.loc[
        categories.category_id.isin(analysis_categories), :
    ]

    tableau = pd.merge(left=prices, right=dates, on='date_id')
    tableau = pd.merge(left=tableau, right=products, on='article')
    tableau = pd.merge(left=tableau, right=subcategories,
                       left_on='first_subcategory', right_on='subcategory_id')
    tableau = pd.merge(left=tableau, right=categories, on='category_id', how='inner')

    tableau = tableau[[
        'date',
        'article',
        'price',
        'discount',
        'subcategory_id',
        'category_id'
    ]]

    tableau_subcategories = subcategories[['subcategory_id', 'subcategory']]
    tableau_categories = categories[['category_id', 'category']]
    tableau_titles = descriptions[['article', 'title']]

    path = '/'.join(
        db_prices_file.split('/')[:-1]
    )
    tableau.to_csv(f'{path}/tableau_prices.csv', index=False)
    tableau_subcategories.to_csv(f'{path}/tableau_subcategories.csv', index=False)
    tableau_categories.to_csv(f'{path}/tableau_categories.csv', index=False)
    tableau_titles.to_csv(f'{path}/tableau_titles.csv', index=False)
    pass
