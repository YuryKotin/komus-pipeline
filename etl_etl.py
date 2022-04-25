import etl_extract as extract
import etl_transform as transform
import etl_load as load

from datetime import datetime


def pipeline(date):
    extract.pipeline(date)
    # transform.pipeline(date)
    # load.pipeline(date)


if __name__ == '__main__':
    # set date
    # date_param = '2022-04-01'
    # or use today
    date_param = datetime.today().strftime('%Y-%m-%d')

    pipeline(date_param)
