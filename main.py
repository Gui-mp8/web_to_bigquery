from models.bigquery import BigQuery
from models.web_scraper import WebScraper
import os

def main():
    json_data = WebScraper(url='https://steamdb.info/sales/').extract_soup_data()
    bigquery = BigQuery('steam-summer-sale', 'summer_sales_data', 'tn_sales_2023')

    return bigquery.load_json_data_to_table(json_data=json_data)


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../web_to_bigquery/models/config.json'
    main()
