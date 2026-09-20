import logging
import pandas as pd


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def clean_customers(customer_df):
    logger.info("Customer cleaning started")

    # Remove duplicates
    customers_df = customer_df.drop_duplicates()
    logger.info("Customer duplicates removed")

    # Handle data types
    customers_df['age'] = customers_df['age'].astype('Int64')

    customers_df['created_at'] = pd.to_datetime(
        customers_df['created_at'],
        errors='coerce'
    )

    logger.info("Data types handled successfully")

    # Handle missing values
    customers_df['name'] = customers_df['name'].fillna('Unknown')
    customers_df['city'] = customers_df['city'].fillna('Unknown')

    customers_df = customers_df.dropna(
        subset=['email', 'age', 'created_at']
    )

    logger.info("Null values removed successfully")

    # Validate email
    valid_email = (
        customers_df['email'].str.contains('@', regex=False)
        & (customers_df['email'].str.count('@') == 1)
        & customers_df['email'].str.endswith('.com')
        & ~customers_df['email'].str.contains(' ', regex=False)
    )

    customers_df.loc[~valid_email, 'email'] = pd.NA
    customers_df = customers_df.dropna(subset=['email'])

    logger.info("Email validation completed")

    # Standardize text fields
    customers_df['name'] = (
        customers_df['name'].str.lower().str.strip()
    )

    customers_df['city'] = (
        customers_df['city'].str.strip().str.title()
    )

    # Validate age
    valid_age = customers_df['age'].between(0, 120)

    customers_df.loc[~valid_age, 'age'] = pd.NA
    customers_df = customers_df.dropna(subset=['age'])

    logger.info("Age validation completed")

    # Validate customer IDs
    if customers_df['customer_id'].is_unique:
        logger.info("Customer ID validation passed")

    logger.info("Customers cleaned successfully")

    return customers_df


def clean_products(products_df):
    logger.info("Products cleaning started")

    # Remove duplicates
    products_df = products_df.drop_duplicates()
    logger.info("Products duplicates removed")

    # Handle data types
    products_df['stock'] = products_df['stock'].astype('Int64')

    products_df['price'] = products_df['price'].replace(
        'free',
        '0'
    )

    products_df['price'] = products_df['price'].astype('float64')

    logger.info("Data types handled successfully")

    # Validate price
    valid_price = products_df['price'] >= 0

    products_df.loc[~valid_price, 'price'] = pd.NA

    logger.info("Price validation completed")

    # Validate stock
    valid_stock = products_df['stock'] >= 0

    products_df.loc[~valid_stock, 'stock'] = pd.NA

    logger.info("Stock validation completed")

    # Standardize product name
    products_df['product_name'] = (
        products_df['product_name'].str.lower().str.strip()
    )

    # Standardize category
    products_df['category'] = (
        products_df['category'].str.strip().str.title()
    )

    # Handle missing values
    products_df['product_name'] = (
        products_df['product_name'].fillna('Unknown')
    )

    products_df['category'] = (
        products_df['category'].fillna('Unknown')
    )

    logger.info("Null values filled successfully")

    # Remove remaining null values
    products_df = products_df.dropna()

    logger.info("Null values removed successfully")

    # Validate product IDs
    if products_df['product_id'].is_unique:
        logger.info("Product ID validation passed")

    logger.info("Products cleaned successfully")

    return products_df


def clean_orders(orders_df, customers_df, products_df):
    logger.info("Orders cleaning started")

    # Remove duplicates
    orders_df = orders_df.drop_duplicates()
    logger.info("Orders duplicates removed")

    # Handle data types
    orders_df['customer_id'] = orders_df['customer_id'].astype('Int64')
    orders_df['product_id'] = orders_df['product_id'].astype('Int64')

    orders_df['quantity'] = orders_df['quantity'].replace(
        'two',
        2
    )

    orders_df['quantity'] = pd.to_numeric(
        orders_df['quantity'],
        errors='coerce'
    ).astype('Int64')

    orders_df['order_date'] = pd.to_datetime(
        orders_df['order_date'],
        errors='coerce'
    )

    logger.info("Data types handled successfully")

    # Validate quantity
    valid_quantity = orders_df['quantity'] > 0

    orders_df.loc[~valid_quantity, 'quantity'] = pd.NA

    logger.info("Quantity validation completed")

    # Validate customer IDs
    valid_customer_id = orders_df['customer_id'].isin(
        customers_df['customer_id']
    )

    orders_df.loc[~valid_customer_id, 'customer_id'] = pd.NA

    logger.info("Customer ID validation completed")

    # Validate product IDs
    valid_product_id = orders_df['product_id'].isin(
        products_df['product_id']
    )

    orders_df.loc[~valid_product_id, 'product_id'] = pd.NA

    logger.info("Product ID validation completed")

    # Handle missing values
    orders_df = orders_df.dropna(
        subset=[
            'order_id',
            'customer_id',
            'product_id',
            'quantity',
            'order_date'
        ]
    )

    logger.info("Null values removed successfully")

    # Validate order IDs
    if orders_df['order_id'].is_unique:
        logger.info("Order ID validation passed")

    logger.info("Orders cleaned successfully")

    return orders_df

