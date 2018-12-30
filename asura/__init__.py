
from random import seed, choice
from io import BytesIO

from .spells import roll_spells
from .esper  import roll_espers

from .data import Esper, Spell, bonus_table, bonuses

def generate(rng=None, mode='snes', forbidden=[]):
    seed(rng)

    if mode == 'snes':
        max_espers = Esper.SNES_Count
        max_spells = Spell.SNES_Count
    else:
        max_espers = Esper.GBA_Count
        max_spells = Spell.GBA_Count

    espers = {}

    data = roll_espers(max_espers)

    for esper in data:
        espers[esper] = {
            'spells': roll_spells(max_spells, forbidden),
            'statup': choice(bonus_table)
        }
        forbidden.extend([i[0] for i in espers[esper]['spells']])

    return espers

remove = [
    (0xA00DE, 5), (0xC7C6D, 11), (0xA55DE, 2), (0xB4DE3, 2),
    (0xB52C9, 2), [0xB5452,  2], (0xA5A2C, 2), (0xB5B77, 2),
    (0xB9A7C, 2), [0xC1ED1,  2], (0xC1F85, 2), (0xC2044, 2),
    (0xC316C, 2), [0xC37A8,  2], (0xC4ADA, 2), (0xC5E08, 2),
    (0xC79D9, 2), [0xC79E9,  2], (0xCD78F, 2)
]

def write_rom(input_name, output_name, mode, espers):
    if mode == 'gba':
        offset = 0x70000
        spello = 0x62A480
        remove.extend(((0xD2B52, 2), (0xD2BD4, 2), (0xD11ED, 2), (0xD27A5,)))
    else:
        spello = 0x186e00

    rom = BytesIO()
    with open(input_name, mode='rb') as f:
        rom.write(f.read())

    # empty the slots we're not using
    for i in remove:
        rom.seek(i[0] + offset, 0)
        rom.write(b'\xFD' * i[1])

    esper_list = espers.keys()

    # these four are the espers given when you reach Tina in Zozo
    rom.seek(0xAA824 + offset, 0); rom.write(bytes([esper_list[0] + 0x36]))
    rom.seek(0xAAC9C + offset, 0); rom.write(bytes([esper_list[1] + 0x36]))
    rom.seek(0xAACAB + offset, 0); rom.write(bytes([esper_list[2] + 0x36]))
    rom.seek(0xAACBA + offset, 0); rom.write(bytes([esper_list[3] + 0x36]))

    for i in range(4):
        esper = esper_list[i]
        spells = espers[esper]['spells']
        statup = espers[esper]['statup']

        leftover = 5 - len(spells)

        rom.seek(spello + esper * 11, 0)
        for spell in spells:
            rom.write(bytes(spell[1], spell[0]))

        if leftover > 0:
            rom.write(b'\x00\xFF' * leftover)
        rom.write(bytes([statup]))

    rom.seek(0, 0)

    with open(output_name, mode='wb') as f:
        f.write(rom.read())

def write_spoilers(filename, espers, rng):
    with open(filename, mode='wt', encoding='utf8') as f:
        f.write('Seed: {}\n\n'.format(rng))

        for esper in espers:
            f.write('{} ({})\n'.format(
                str(esper).split('.')[1],
                str(espers[esper]['statup']).split('.')[1]
            ))
            for spell in espers[esper]['spells']:
                f.write('  {} ×{}\n'.format(
                    str(spell[0]).split('.')[1],
                    spell[1]
                ))
            f.write('\n')
