from google.cloud import bigquery
from typing import Dict

class Bigquery():
    def __init__(self,config_path: Dict[str, str]) -> None:
        self.client = bigquery.Client.from_service_account_json(config_path)


client = Bigquery(config_path='/home/guilherme/Documentos/vscode/web_to_bigquery/config.json')
project_id = ''
dataset_id='steam_summer_sales_2023'
dataset = bigquery.Dataset(dataset_id)

created_dataset = client.create_dataset(dataset, exists_ok=True)
if created_dataset:
    print('Dataset created successfully.')
else:
    print('Dataset already exists.')