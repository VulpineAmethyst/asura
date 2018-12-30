
from random import randint
from .data import Spell, slots, slots_gba

def roll_spells(max, forbidden=()):
    count = 8
    n = 5
    spells = []
    spells_got = list(forbidden)

    while True:
        if n <= 0 or count <= 0:
            break

        spell = Spell(randint(0, max))

        if spell in spells_got:
            continue

        if (count - slots[spell]) >= 0:
            spells.append([spell, randint(1, 5 - slots[spell]) * 5])
            spells_got.append(spell)
            count -= slots
            n -= 1

    return spells
