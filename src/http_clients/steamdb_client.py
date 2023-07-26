import requests
from http_clients.steamdb_client_config import SteamDbClientConfig


class SteamDbClient():
    def __init__(self, client_config: SteamDbClientConfig) -> None:
        self.__url: str = "https://steamdb.info/"
        self.__sales_page_path: str = "sales/"
        self.headers: dict = {
            "Cookie": client_config.get_cookie_header_text(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }

    def get_sales_page_html_bytes(self) -> bytes:
        try:
            response: requests.Response = requests.get(url=f"{self.__url}{self.__sales_page_path}", headers=self.headers)
            if response.status_code != 200:
                    return ""
            return response.content
                # logger.error(
                    # "The error is on headers, you must change the 'accept', 'cokie' and 'user-agent' params")
            # logger.info(f'STATUS CODE: {response.status_code}')
        except Exception:
            raise

# 
