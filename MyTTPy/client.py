from . import parser
from pathlib import Path

from .player import Player
from .request_handler import RequestHandler


class MyTTClient:
    def __init__(self):
        self.handler = RequestHandler()
        self.handler.check_for_cookies()
        self.logged_in = self.handler.logged_in

    def log_in(self, username: str, password: str):
        self.logged_in = self.handler.log_in(username, password)
        return self.logged_in

    def get_players(self, first_name: str, last_name: str) -> list[Player]:
        player_list = self.handler.get_player_list(first_name, last_name)
        players = parser.parse_players_from_json(player_list)
        for index, player in enumerate(players):
            player_qttr_history = self.handler.get_qttr_history_page(player.id)
            player.qttr = parser.parse_qttr(player_qttr_history)
            if(player.qttr == -1):
                players.pop(index)

        return players

    def get_player(self, first_name: str, last_name: str, club_name: str = None) -> Player:
        players = self.get_players(first_name, last_name)

        if(len(players) == 1):
            return players[0]

        for player in players:
            if(club_name.lower() in player.club_name.lower()):
                return player
        
        return None
