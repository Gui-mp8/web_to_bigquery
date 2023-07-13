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

class WebScraper():
    def __init__(self, url: str) -> None:
        self.url = url
        self.session = None
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "cookie": "cf_clearance=k4R7jAe2EKTktPjEgATVzuehYw.SHgoYKYO8aL7It6s-1689216169-0-160; __cf_bm=AC16fBICbYUwSK.G.ce9sRT0I0KQ62fD1GdU4_AcI00-1689217358-0-AZhkYuQPFWxQz/Om1JR4Z9KvKdgsZSaYP9NruJChDHglGOt/E4jI3aRzn/rqtbOJtOmcjKHb9HisZBZk9R1JvJs=",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
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
        return self.create_session().get(url=self.url, headers=self.headers)

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.response().content, 'html.parser')

    def extract_soup_data(self) -> List[Dict[str, Any]]:
        data_sort_keys = ['game_name','discount', 'price', 'rating', 'end_date', 'start_date', 'release_date']

        blocks = self.soup().find_all('tr', class_='app')
        data_list = []

        for block in blocks:
            data_sort_values = block.find_all('td', {'data-sort': True})

            game_name_tag = block.find('a', class_='b')
            game_name = game_name_tag.get_text()

            data_sort_dict = dict(zip(data_sort_keys, [game_name] + [tag['data-sort'] for tag in data_sort_values][-6:]))
            data_list.append(data_sort_dict)
            self.logger.info(data_sort_dict)

        return json.dumps(data_list)
