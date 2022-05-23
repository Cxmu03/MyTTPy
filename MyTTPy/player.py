from dataclasses import dataclass

@dataclass
class Player:
    name: str
    id: int
    qttr: int
    club_name: str
    club_id: int