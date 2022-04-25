import pandas as pd
from sqlalchemy import create_engine, inspect

from schema import *

if __name__ == '__main__':
    engine = create_engine('postgresql://yury:1234@localhost/komus')
    inspector = inspect(engine)

    tables = [
        (db_categories_file, 'categories'),
        (db_subcategories_file, 'subcategories'),
        (db_dates_file, 'dates'),
        (db_products_file, 'products'),
        (db_prices_file, 'prices'),
        (db_descriptions_file, 'descriptions')
    ]

    table_names =inspector.get_table_names()
    if len(table_names) > 0:
        with engine.begin() as conn:
            for table in tables[::-1]:
                sql = f'delete from {table[1]}'
                conn.execute(sql)
            # print(table_names)

    [
        pd.read_csv(
            table[0], index_col=0
        ).to_sql(
            table[1], con=engine, index=False, if_exists='append'
        )
        for table in tables
    ]
