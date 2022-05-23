import json

from bs4 import BeautifulSoup

from .player import Player

HTML_PARSER = "html.parser"

def parse_player(player: str) -> Player:
    player_name = f"{player['firstname']} {player['lastname']}"
    player_id = player["personId"]
    club_info = player["club"]
    club_name = club_info["name"]
    club_id = club_info["nr"]
    return Player(player_name, player_id, 0, club_name, club_id)

def parse_players_from_json(jsonString: str) -> list[Player]:
    players = []
    jsonObj = json.loads(jsonString)

    for player in jsonObj["items"]:
        players.append(parse_player(player))

    return players

def check_if_login_site(page: str) -> bool:
    soup = BeautifulSoup(page, HTML_PARSER)
    if("Login" in str(soup.title)):
        return True
    
    return False

def parse_qttr(page: str) -> int:
    soup = BeautifulSoup(page, HTML_PARSER)
    ttr_box = soup.select_one(".ttr-box")
    if(ttr_box == None):
        return -1
    return int(ttr_box.find(lambda tag: tag.name == "span" and "Q-TTR" in tag.text).next_sibling)
