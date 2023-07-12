import os
from google.cloud import bigquery
import json
from web_scraper import WebScraper

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'config.json'

def create_dataset(project_name, dataset_name):
    client = bigquery.Client()

    dataset_id = f"{project_name}.{dataset_name}"
    dataset = client.get_dataset(dataset_id)

    if not dataset:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        dataset = client.create_dataset(dataset)  # Make an API request.
        print(f"Created dataset {dataset.project}.{dataset.dataset_id}")
    else:
        print(f"Dataset {dataset_id} already exists")

def create_table(project_name, dataset_name, table_name):
    client = bigquery.Client()

    schema = [
        bigquery.SchemaField("game_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("discount", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("price", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("rating", "STRING", mode="REQUIRED"),
    ]

    table_id = f"{project_name}.{dataset_name}.{table_name}"
    table_path = bigquery.Table(table_id, schema=schema)

    if not client.get_table(table_path, retry=None):
        table = client.create_table(table_path)  # Make an API request.
        print(f"Created table {table.full_table_id}")
    else:
        print(f"Table {table_id} already exists")

def load_json_data_to_table(project_name, dataset_name, table_name, json_data):
    client = bigquery.Client()

    table_id = f"{project_name}.{dataset_name}.{table_name}"
    table_ref = client.get_table(table_id)

    # Load JSON data into table
    rows = json.loads(json_data)
    errors = client.insert_rows_json(table_ref, rows)

    if len(errors) == 0:
        print("JSON data loaded successfully.")
    else:
        print("Encountered errors while loading JSON data:")
        for error in errors:
            print(error)

# json_data = WebScraper(url='https://steamdb.info/sales/').extract_soup_data()
# load_json_data_to_table('steam-summer-sale', 'summer_sales_data', 'tn_sales_2023',json_data=json_data)