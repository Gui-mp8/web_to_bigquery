import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

from google.cloud import bigquery
import json
from typing import Dict, Any

class BigQuery():
    def __init__(self, project_name:str, dataset_name:str, table_name:str) -> None:
        self.client = bigquery.Client()
        self.dataset_id = f"{project_name}.{dataset_name}"
        self.table_id = f"{project_name}.{dataset_name}.{table_name}"
        self.logger = logging.getLogger(__name__)

    def create_dataset(self) -> bigquery.Dataset:
        try:
            dataset = self.client.get_dataset(self.dataset_id)
        except Exception:
            dataset = False

        if not dataset:
            dataset = bigquery.Dataset(self.dataset_id)
            dataset.location = "US"
            dataset = self.client.create_dataset(dataset)

            self.logger.info(f"Created dataset {self.dataset_id}")
        else:
            self.logger.info(f"Dataset {self.dataset_id} already exists")

    def create_table(self) -> bigquery.Table:
        schema = [
            bigquery.SchemaField("game_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("discount", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("price", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("rating", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("end_date", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("start_date", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("release_date", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("extract_date", "STRING", mode="REQUIRED")
        ]
        table_path = bigquery.Table(self.table_id, schema=schema)

        try:
            table = self.client.get_table(table_path, retry=None)
        except Exception:
            table = False

        if not table:
            table = self.client.create_table(table_path)  # Make an API request.
            self.logger.info(f"Created table {table.full_table_id}")
        else:
            self.logger.info(f"Table {self.table_id} already exists")

    def is_table_empty(self, table_ref) -> bool:
        query_job = self.client.query(f"SELECT COUNT(*) FROM {table_ref}")
        result = query_job.result()
        row_count = next(result).values()[0]
        return row_count == 0

    def load_json_data_to_table(self, json_data: Dict[str, Any]) -> None:
        table_ref = self.client.get_table(self.table_id)
        rows = json.loads(json_data)

        # Check if the table has existing data
        if self.is_table_empty(table_ref):
            self.client.insert_rows_json(table_ref, rows)
        else:
            self.logger.info("Table already has data. Skipping insertion.")
