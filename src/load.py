import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def load_csv(final_df):

    logger.info("Loading data to CSV")

    output_path = Path(r'E:\ETL-Project\output\csv')
    output_path.mkdir(parents=True, exist_ok=True)

    final_df.to_csv(
        output_path / 'final_data.csv',
        index=False
    )

    logger.info("Final data saved successfully")
