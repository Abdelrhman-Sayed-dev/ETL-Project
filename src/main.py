import logging

from extract import extract
from cleaning import (
    clean_customers,
    clean_products,
    clean_orders
)
from transform import transform
from load import load_csv

def main():

    # Extract
    customer_df, product_df, orders_df = extract()

    # Cleaning
    customer_df = clean_customers(customer_df)
    product_df = clean_products(product_df)

    orders_df = clean_orders(
        orders_df,
        customer_df,
        product_df
    )

    # Transformation
    final_df = transform(
        customer_df,
        product_df,
        orders_df
    )

    load_csv(final_df)

    
if __name__ == "__main__":
    main()
