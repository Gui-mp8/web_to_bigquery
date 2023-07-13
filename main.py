from models.bigquery import BigQuery
from models.web_scraper import WebScraper
import os

def main(project_name, dataset_name, table_name):
    json_data = WebScraper(url='https://steamdb.info/sales/').extract_soup_data()

    bq = BigQuery(project_name, dataset_name, table_name)
    bq.create_dataset()
    bq.create_table()
    bq.load_json_data_to_table(json_data=json_data)


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'config.json'
    main(
        project_name='summer-sales-extraction1',
        dataset_name='summer_sales_data',
        table_name='tn_sales_2023'
    )

