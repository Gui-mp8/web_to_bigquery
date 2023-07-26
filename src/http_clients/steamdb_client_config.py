class SteamDbClientConfig:
    __cf_clearance: str
    __cf_bm: str
    __cf_chl_2: str

    def __init__(self, cf_clearance: str, cf_bm: str, cf_chl_2: str):
        self.__cf_clearance = cf_clearance
        self.__cf_bm = cf_bm
        self.__cf_chl_2 = cf_chl_2

    def get_cookie_header_text(self) -> str:
        return f"cf_clearance={self.__cf_clearance};__cf_bm={self.__cf_bm};cf_chl_2={self.__cf_chl_2}"
