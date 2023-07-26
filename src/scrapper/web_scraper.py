from urllib3 import Retry
import requests
from requests.adapters import HTTPAdapter
from requests.sessions import Session

from bs4 import BeautifulSoup
import json
from typing import Dict, List, Any
from datetime import datetime
from http_clients.steamdb_client import SteamDbClient

from logger.logger import Loggador

class SteamDbScraper():
    def __init__(self, steamClient: SteamDbClient, logger: Loggador) -> None:
        self.__logger: Loggador = logger
        self.__steamClient: SteamDbClient = steamClient

    def extract_soup_data(self) -> List[Dict[str, Any]]:
        sales_page_bytes: bytes = self.__steamClient.get_sales_page_html_bytes()
        soup = BeautifulSoup(sales_page_bytes, 'html.parser')

        data_sort_keys: list = [
            'game_name',
            'discount', 
            'price', 
            'rating', 
            'end_date', 
            'start_date', 
            'release_date', 
            'extract_date'
        ]

        blocks = soup.find_all('tr', class_='app')
        
        data_list_dict = []
        for block in blocks:
            data_sort_values = block.find_all('td', {'data-sort': True})

            game_name_tag = block.find('a', class_='b')
            game_name = game_name_tag.get_text()

            extract_date = datetime.now().strftime("%Y-%m-%d")  # Get the current date

            data_sort_dict = dict(zip(data_sort_keys, [game_name] + [tag['data-sort'] for tag in data_sort_values][-6:] + [extract_date]))
            data_list_dict.append(data_sort_dict)
            self.__logger.LogInfo(data_sort_dict)

        return data_list_dict
