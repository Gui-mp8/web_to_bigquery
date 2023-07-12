from google.cloud import bigquery
import json
from typing import Dict, Any
import os

class BigQuery():
    def __init__(self, project_name:str, dataset_name:str, table_name:str) -> None:
        self.client = bigquery.Client()
        self.dataset_id = f"{project_name}.{dataset_name}"
        self.table_id = f"{project_name}.{dataset_name}.{table_name}"

    def create_dataset(self) -> bigquery.Dataset:
        try:
            dataset = self.client.get_dataset(self.dataset_id)
        except Exception:
            dataset = False

        if not dataset:
            dataset = bigquery.Dataset(self.dataset_id)
            dataset.location = "US"
            dataset = self.client.create_dataset(dataset)

            print(f"Created dataset {self.dataset_id}")
        else:
            print(f"Dataset {self.dataset_id} already exists")

    def create_table(self) -> bigquery.Table:
        schema = [
            bigquery.SchemaField("game_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("discount", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("price", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("rating", "STRING", mode="REQUIRED"),
        ]
        table_path = bigquery.Table(self.table_id, schema=schema)
        
        try:
            table = self.client.get_table(table_path, retry=None)
        except Exception:
            table = False

        if not table:
            table = self.client.create_table(table_path)  # Make an API request.
            print(f"Created table {table.full_table_id}")
        else:
            print(f"Table {self.table_id} already exists")

    def load_json_data_to_table(self, json_data: Dict[str, Any]) -> None:
        table_ref = self.client.get_table(self.table_id)

        # Check if table is empty
        if table_ref.num_rows == 0:
            # Load JSON data into table
            rows = json.loads(json_data)
            errors = self.client.insert_rows_json(table_ref, rows)

            if len(errors) == 0:
                print("JSON data loaded successfully.")
            else:
                print("Encountered errors while loading JSON data:")
                for error in errors:
                    print(error)
        else:
            print("Table is not empty. Skipping data load.")
