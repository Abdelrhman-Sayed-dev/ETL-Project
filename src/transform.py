import logging


logger = logging.getLogger(__name__)


def transform(customer_df, product_df, orders_df):

    logger.info("Data transformation started")

    # Merge orders with customers
    merged_df = orders_df.merge(
        customer_df,
        on='customer_id',
        how='inner'
    )

    # Merge with products
    final_df = merged_df.merge(
        product_df,
        on='product_id',
        how='inner'
    )

    final_df['total_amount'] = (
            final_df['quantity'] * final_df['price']
    )

    logger.info("Data transformation completed successfully")

    return final_df
