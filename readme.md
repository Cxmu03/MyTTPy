# MyTTPy
This repository tries to be sort of an unofficial API for mytischtennis.de by parsing the website contents
# Example Usage
```py
>>> from MyTTPy import client
>>> client = MyTTClient()
>>> client.log_in("username", "password")
>>> player = client.get_player("Timo", "Boll", "Dürkheim")
>>> player
Player(name='Timo Boll', id='17741', qttr=2595, club_name='Borussia Düsseldorf', club_id='141046')
```
# MyTTClient
The MyTTClient defines several functions which can be used to extract information about a player, a club, a league (Not yet implemented) etc.

```py
MyTTClient.log_in(username: str, password: str) -> bool
```
<ul>
Tries to log in with the given credentials and returns whether or not the login process succeeded. If login succeeds, the cookies are stored in an external file and automatically checked for validity when the MyTTClient constructor is being called.
</ul>

```py
MyTTClient.get_players(first_name: str, last_name: str) -> list[Player]
```
<ul>
Returns all the players with a matching (or similar) name.
</ul>

```py
MyTTClient.get_player(first_name: str, last_name: str, club_name: str) -> Player
```
<ul>
Looks up a player by their name and checks if the provided club name is contained in any of the clubnames of the player list.
</ul>

# TODO
- Asynchronous requests with HTTPX
- Club support
- League support
- TTR History
- Ranking support
# Disclaimer
I take no responsibility for misuse of this code and consequenses arising from such conduct. This is purely for educational purposes. **Any possible account ban does not fall into my responsibility**.
