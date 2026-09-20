from pathlib import Path
import pandas as pd

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s' , level=logging.INFO)
logger = logging.getLogger(__name__)

path = Path(r'E:\ETL-Project\raw_data')


def extract():
    logger.info('data extraction start')

    customers_df =pd.read_csv(path/'customers.csv')
    logger.info("customers extracted successfully")

    products_df =pd.read_csv(path/'products.csv')
    logger.info("products extracted successfully")

    orders_df = pd.read_csv(path/'orders.csv')
    logger.info("orders extracted successfully")

    return customers_df, products_df, orders_df