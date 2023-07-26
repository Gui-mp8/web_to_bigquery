import json
from http_clients.steamdb_client import SteamDbClient
from http_clients.steamdb_client_config import SteamDbClientConfig
from logger.logger import Loggador, MyLogger
from big_query.big_query import BigQuery
from etl.etl import transforming_json
import os

from scrapper.web_scraper import SteamDbScraper

class Main:
    def __init__(self):
        self.__setup()

    def __setup(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'config.json'
        self.load_configurations()
        self.__logger: Loggador = MyLogger()
        steam_db_config = SteamDbClientConfig(
            self.configuration["steamdb_client_config"]["cf_clearance"], 
            self.configuration["steamdb_client_config"]["cf_bm"],
            self.configuration["steamdb_client_config"]["cf_chl_2"])
        self.__steam_client = SteamDbClient(steam_db_config)
        self.__steam_scrapper = SteamDbScraper(self.__steam_client, self.__logger)
        
    def load_configurations(self) -> None:
        with open("settings.json", "r") as json_config_file:
            self.configuration = json.load(json_config_file)

    def run(self):
        extracted_values = self.__steam_scrapper.extract_soup_data()
        # json_data = transforming_json(json_data)
        # bq = BigQuery(project_name, dataset_name, table_name)
        # bq.create_dataset()
        # bq.create_table()
        # bq.load_json_data_to_table(json_data=json_data)

# def main(project_name, dataset_name, table_name):
def main():
    program = Main()
    program.run()

    # json_data = transforming_json(json_data)
    # bq = BigQuery(project_name, dataset_name, table_name)
    # bq.create_dataset()
    # bq.create_table()
    # bq.load_json_data_to_table(json_data=json_data)


if __name__ == "__main__":
    main()
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'config.json'
    # main(
    #     project_name='summer-sales-extraction1',
    #     dataset_name='summer_sales_data',
    #     table_name='tn_sales_2023'
    # )

