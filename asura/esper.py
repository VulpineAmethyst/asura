
from random import sample

from .data import Esper

def roll_espers(max):
    return [Esper(i) for i in sample(list(range(max)), 4)]