import pickle
import time
import urllib.parse
from pathlib import Path

from requests import Session
from requests.cookies import RequestsCookieJar

from . import parser
from .global_urls import BASE_PAGE, LOGIN_PAGE, LOGIN_REDIRECT_PAGE, TTR_HISTORY_PAGE


class RequestHandler:
    def __init__(self):
        self.session = Session()
        self.logged_in = False
        self.check_for_cookies()

    def log_in(self, username: str, password: str) -> bool:
        data = {
            "userNameB": username,
            "userPassWordB": password,
            "permalogin": "1",
            "targetPage": LOGIN_REDIRECT_PAGE
        }

        response = self.session.post(LOGIN_PAGE, data=data)

        if response.status_code != 200:
            return False

        with open("cookies.bin", "wb") as cookie_file:
            pickle.dump(self.session.cookies, cookie_file)

        self.logged_in = True
        return self.logged_in

    def check_for_cookies(self) -> bool:
        if not Path("cookies.bin").exists():
            return False

        with open("cookies.bin", "rb") as cookie_file:
            cookie_jar: RequestsCookieJar = pickle.load(cookie_file)

        for cookie in cookie_jar:
            if((cookie.expires is not None) and (cookie.expires < int(time.time()))):
                return False

        self.session.cookies = cookie_jar

        if not self.test_cookies():
            self.session.cookies = None
            return False

        self.logged_in = True
        return True

    def test_cookies(self) -> bool:
        response = self.get_page(TTR_HISTORY_PAGE)
        return not parser.check_if_login_site(response)

    def get_page(self, url: str) -> str:
        response = self.session.get(url)
        return response.text

    def get_player_list(self, first_name: str, last_name: str) -> str:
        first_name = urllib.parse.quote_plus(first_name)
        last_name = urllib.parse.quote_plus(last_name)
        url = f"{BASE_PAGE}/clicktt/PTTV/player/search?firstResult=0&maxResults=50&firstname={first_name}&lastname={last_name}"
        return self.get_page(url)

    def get_qttr_history_page(self, player_id: int) -> str:
        url = f"{TTR_HISTORY_PAGE}?personId={player_id}"
        return self.get_page(url)
