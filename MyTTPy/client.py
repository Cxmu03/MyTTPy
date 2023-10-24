from . import parser
from .player import Player
from .request_handler import RequestHandler

from typing import Optional


class MyTTClient:
    '''
    A MyTTClient provides the API to the mytischtennis.de website by giving access to players and clubs.
    '''
    def __init__(self):
        self.handler = RequestHandler()
        self.handler.check_for_cookies()
        self.logged_in = self.handler.logged_in

    def log_in(self, username: str, password: str):
        '''
        Logs the client in with the passed credentials

        Parameters
        ----------
        username: str
            The username for logging in
        password: str
            The password for logging in

        Returns
        -------
        bool
            Whether or not the login was successful
        '''
        self.logged_in = self.handler.log_in(username, password)
        return self.logged_in

    def get_players(self, first_name: str, last_name: str) -> list[Player]:
        '''
        Retrieves a list of players with matching first or last names

        Parameters
        ----------
        first_name: str
            First name of the player you are searching for
        last_name: str
            Last name of the player you are searching for

        Returns
        -------
        list[Player]
            A list of players with similar names
        '''
        player_list = self.handler.get_player_list(first_name, last_name)
        players = parser.parse_players_from_json(player_list)
        for index, player in enumerate(players):
            player_qttr_history = self.handler.get_qttr_history_page(player.id)
            player.qttr = parser.parse_qttr(player_qttr_history)
            if player.qttr == -1:
                players.pop(index)

        return players

    def get_player(self, first_name: str, last_name: str, club_name: str = None) -> Optional[Player]:
        '''
        Retrieves a player associated with a specific club

        Parameters
        ----------
        first_name: str
            First name of the player you are searching for
        last_name: str
            Last name of the player you are searching for
        club_name: str
            Name of the club that the player is in, by default None

        Returns
        -------
        Optional[Player]
            A Player object if a matching player could be found, None otherwise
        '''
        players = self.get_players(first_name, last_name)

        if len(players) == 1 or club_name is None:
            return players[0]

        for player in players:
            if club_name.lower() in player.club_name.lower():
                return player

        return None
