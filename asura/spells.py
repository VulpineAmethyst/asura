
from random import randint
from .data import Spell, slots, slots_gba

def roll_spells(cap, forbidden=()):
    count = 6
    n = 5
    spells = []
    spells_got = list(forbidden)

    while True:
        if n <= 0 or count <= 0:
            break

        spell = Spell(randint(0, cap))

        if spell in spells_got:
            continue

        if (count - slots[spell]) >= 0:
            spells.append([spell, randint(1, max(6 - slots[spell], 2)) * 5])
            spells_got.append(spell)
            count -= slots[spell]
            n -= 1

    return spells
