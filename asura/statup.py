
from random import sample

from .data import bonus_table

def roll_statup():
    return [Bonus(i) for i in sample(list(bonus_table), 4)]