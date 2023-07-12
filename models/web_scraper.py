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
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "cookie": "cf_chl_2=0f811a9aa1e21cc; cf_clearance=W5hoD.mM4zzqMAMgk1IutY3NkRv0flJp1ro6zd9cKQM-1689161684-0-160; __cf_bm=2RWpCjNQjXgiKKF7PQelB8fDQgvXeIr4ncKtOPIYrX0-1689164681-0-AeKP7HJ5WShG2VnaFmHwCtcGDKlbhU+lHZlY+wu4m7xcKYbJC/RmkIoBgGobHa5mqQ7lsowjjRvDbWcOqaa2Tw0=",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
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

    # def random(self):
    #     self.headers['User-Agent'] = random.choice(self.user_agents)
    #     print(self.headers)
    #     return self.headers

    def response(self) -> requests.Response:
        return self.create_session().get(url=self.url, headers=self.headers)

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.response().content, 'html.parser')

    def extract_soup_data(self) -> List[Dict[str, Any]]:
        items = self.soup().find_all('td')

        game_dict_list = []

        for item in items:
            game_name = item.find('a', class_='b')

            if game_name is not None and game_name['target'] == '_blank':
                game_dict = {'game_name': str(game_name.string)}  # Create a new dictionary for each game
                game_dict_list.append(game_dict)  # Append the dictionary to the list

            elif 'data-sort' in item.attrs:
                value = item.get_text(strip=True)

                if value.startswith('-') and value.endswith('%'):
                    if len(game_dict_list) > 0 and 'discount' not in game_dict_list[-1]:
                        game_dict_list[-1]['discount'] = str(value)
                    else:
                        game_dict = {'discount': str(value)}
                        game_dict_list.append(game_dict)



                elif value.startswith('R$'):
                    if len(game_dict_list) > 0 and 'price' not in game_dict_list[-1]:
                        game_dict_list[-1]['price'] = str(value)
                    else:
                        game_dict = {'price': str(value)}
                        game_dict_list.append(game_dict)



                elif not value.startswith('-') and value.endswith('%'):
                    if len(game_dict_list) > 0 and 'rating' not in game_dict_list[-1]:
                        game_dict_list[-1]['rating'] = str(value)
                    else:
                        game_dict = {'rating': str(value)}
                        game_dict_list.append(game_dict)
                    self.logger.info(game_dict)

        return json.dumps(game_dict_list)
    