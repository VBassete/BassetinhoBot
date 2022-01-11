from dataclasses import dataclass
from bson.objectid import ObjectId

@dataclass(init=True)
class Player:
    '''Classe para armazenar os dados de um Jogador da dungeon'''
    _id: ObjectId
    Player_id: int
    Player_name: str
    Class: str
    Subclass: int
    Wins: int
    Loses: int
    XP: int
    LVL: int
    Cooldown: float
