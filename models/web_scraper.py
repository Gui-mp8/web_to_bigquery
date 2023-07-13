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

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.sessions import Session

from bs4 import BeautifulSoup
import json
from typing import Dict, List, Any
from datetime import datetime

class WebScraper():
    def __init__(self, url: str) -> None:
        self.url = url
        self.session = None
        self.logger = logging.getLogger(__name__)

    def create_session(self) -> Session:
        session = self.session

        if session is None:
            session = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=2,
                            status_forcelist=[500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

        return session

    def response(self) -> requests.Response:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "cookie": "cf_clearance=W5hoD.mM4zzqMAMgk1IutY3NkRv0flJp1ro6zd9cKQM-1689161684-0-160; __cf_bm=2LUm5F5Ziw0Zrfl7MS62b9xBkwjziROWKoWtQyiLlp8-1689252045-0-AXFz599NwACtjBOsXiP16LZjUSm/xsQYaxNzGf6VCYI6CnmhU0Lz2oUa/9nRdTJKXh4jruwbAGB0mIO6Hrxys8U=",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
        }
        try:
            response = self.create_session().get(url=self.url, headers=headers)
            if response.status_code != 200:
                logger.error("The error is on headers, you must change the 'accept', 'cokie' and 'user-agent' params")
            logger.info(f'STATUS CODE: {response.status_code}')
        except Exception:
            raise

        return response

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.response().content, 'html.parser')

    def extract_soup_data(self) -> List[Dict[str, Any]]:
        data_sort_keys = ['game_name','discount', 'price', 'rating', 'end_date', 'start_date', 'release_date', 'extract_date']

        blocks = self.soup().find_all('tr', class_='app')
        data_list_dict = []

        for block in blocks:
            data_sort_values = block.find_all('td', {'data-sort': True})

            game_name_tag = block.find('a', class_='b')
            game_name = game_name_tag.get_text()

            extract_date = datetime.now().strftime("%Y-%m-%d")  # Get the current date

            data_sort_dict = dict(zip(data_sort_keys, [game_name] + [tag['data-sort'] for tag in data_sort_values][-6:] + [extract_date]))
            data_list_dict.append(data_sort_dict)
            self.logger.info(data_sort_dict)

        return data_list_dict
