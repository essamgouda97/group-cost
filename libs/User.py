# TODO 

from __future__ import annotations
from typing import Dict, Any

class User:
    def __init__(self,username: str):
        self.username = username
        self.money_from: Dict[User, int] = {}


    def add_money_from(self, username: User, amount: int):
        self.money_from[username] = amount


