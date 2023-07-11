import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Any

class WebScraper():
    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
                        'authority': 'steamdb.info',
                        'method': 'GET',
                        'path': '/sales/',
                        'scheme': 'https',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                        'cache-control': 'max-age=0',
                        'cookie': 'cf_clearance=Y4WqHMPgt6Wsp3IH8zfYjpcYONIDMySjmMKNXD7mYIM-1689072343-0-250; __cf_bm=DBIwIE7oOga.Wb3XxEh.RucCd8UqA8x7LYLQMqE0k1o-1689075723-0-Aa88zwjAHRK0XpzHtO4XbZI1u6XI04prU4AXijY6Ligs9SnHpK7seV56aPAJXrGju2eBBrFS3uJCiS/uU1mbhFg=',
                        'sec-ch-ua': '"Opera";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Linux"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
                        }

    def response(self) -> requests.Response:
        return requests.get(url=self.url, headers=self.headers)

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

        return game_dict_list
