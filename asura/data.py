#!/usr/bin/env python3
#
# Copyright (C) 2019 Kiyoshi Aman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
#
# This project was made possible by:
# * Lenophis, who told me where the 'give this esper' bytes are
# * ff6hacking.com, which hosts the data tables I used to pick from.
# * CanOfWorms, for figuring out the GBA offsets.
#
# ChangeLog:
# 0.3:
# - GBA support! Purportedly works for J, U, *and* E versions.
# 0.2:
# - Preliminary work toward supporting GBA ROMs. This needs data I
#   don't have to complete, however, but the cleanup it required was
#   useful.
# - Reworked learning rates. Rates should be overall lower now.
# - Majority of output moved to a spoilers file.

from copy import copy
from enum import IntEnum

class Bonus(IntEnum):
    HP_10 = 0x00
    HP_30 = 0x01
    HP_50 = 0x02
    MP_10 = 0x03
    MP_30 = 0x04
    MP_50 = 0x05
    HP100 = 0x06
    LV_30 = 0x07
    LV_50 = 0x08
    Str_1 = 0x09
    Str_2 = 0x0A
    Spd_1 = 0x0B
    Spd_2 = 0x0C
    Vit_1 = 0x0D
    Vit_2 = 0x0E
    Mag_1 = 0x0F
    Mag_2 = 0x10
    Nil   = 0xFF

bonuses = {
    Bonus.HP_10: 'HP +10%',
    Bonus.HP_30: 'HP +30%',
    Bonus.HP_50: 'HP +50%',
    Bonus.MP_10: 'MP +10%',
    Bonus.MP_30: 'MP +30%',
    Bonus.MP_50: 'MP +50%',
    Bonus.HP100: 'HP +100%',
    Bonus.Str_1: 'Strength +1',
    Bonus.Str_2: 'Strength +2',
    Bonus.Spd_1: 'Speed +1',
    Bonus.Spd_2: 'Speed +2',
    Bonus.Mag_1: 'Magic +1',
    Bonus.Mag_2: 'Magic +2',
}
bonus_table = [
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_30, Bonus.MP_30,
    Bonus.HP_30, Bonus.MP_30,
    Bonus.HP_30, Bonus.MP_30,
    Bonus.HP_50, Bonus.MP_50,
    Bonus.HP_50, Bonus.MP_50,
    Bonus.Str_1, Bonus.Mag_1, Bonus.Spd_1,
    Bonus.Str_1, Bonus.Mag_1, Bonus.Spd_1,
    Bonus.Str_2, Bonus.Mag_2, Bonus.Spd_2,
    Bonus.HP100,
    Bonus.Str_2, Bonus.Mag_2, Bonus.Spd_2,
    Bonus.Str_1, Bonus.Mag_1, Bonus.Spd_1,
    Bonus.Str_1, Bonus.Mag_1, Bonus.Spd_1,
    Bonus.HP_50, Bonus.MP_50,
    Bonus.HP_50, Bonus.MP_50,
    Bonus.HP_30, Bonus.MP_30,
    Bonus.HP_30, Bonus.MP_30,
    Bonus.HP_30, Bonus.MP_30,
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_10, Bonus.MP_10,
    Bonus.HP_10, Bonus.MP_10,
]

class Spell(IntEnum):
    Fire       = 0x00
    Blizzard   = 0x01
    Thunder    = 0x02
    Poison     = 0x03
    Drain      = 0x04
    Firera     = 0x05
    Blizzardra = 0x06
    Thunderra  = 0x07
    Bio        = 0x08
    Firega     = 0x09
    Blizzardga = 0x0A
    Thunderga  = 0x0B
    Break      = 0x0C
    Death      = 0x0D
    Holy       = 0x0E
    Flare      = 0x0F
    Gravity    = 0x10
    Gravityga  = 0x11
    Dezone     = 0x12
    Meteor     = 0x13
    Ultima     = 0x14
    Quake      = 0x15
    Tornado    = 0x16
    Meltdown   = 0x17
    Library    = 0x18
    Slow       = 0x19
    Rasp       = 0x1A
    Silence    = 0x1B
    Protect    = 0x1C
    Sleep      = 0x1D
    Confuse    = 0x1E
    Haste      = 0x1F
    Stop       = 0x20
    Berserk    = 0x21
    Float      = 0x22
    Kappa      = 0x23
    Reflect    = 0x24
    Shell      = 0x25
    Vanish     = 0x26
    Hastega    = 0x27
    Slowga     = 0x28
    Osmose     = 0x29
    Warp       = 0x2A
    Quick      = 0x2B
    Dispel     = 0x2C
    Cure       = 0x2D
    Curera     = 0x2E
    Curega     = 0x2F
    Raise      = 0x30
    Arise      = 0x31
    NullPoison = 0x32
    NullStatus = 0x33
    Regen      = 0x34
    Reraise    = 0x35

    Flood     = 54
    Gravityja = 55
    Valor     = 56

    SNES_Count = 54
    GBA_Count  = 57

spell_map = {
    'Fire':         Spell.Fire,
    'Blizzard':     Spell.Blizzard,
    'Ice':          Spell.Blizzard,
    'Thunder':      Spell.Thunder,
    'Bolt':         Spell.Thunder,
    'Poison':       Spell.Poison,
    'Firera':       Spell.Firera,
    'Fira':         Spell.Firera,
    'Fire2':        Spell.Firera
    'Blizzardra':   Spell.Blizzardra,
    'Blizzara':     Spell.Blizzardra,
    'Ice2':         Spell.Blizzardra,
    'Thunderra':    Spell.Thunderra,
    'Thundera':     Spell.Thunderra,
    'Thundara':     Spell.Thunderra,
    'Bolt2':        Spell.Thunderra,
    'Bio':          Spell.Bio,
    'Firega':       Spell.Firega,
    'Figa':         Spell.Firega,
    'Firaga':       Spell.Firega,
    'Fire3':        Spell.Firega,
    'Blizzardga':   Spell.Blizzardga,
    'Blizzaga':     Spell.Blizzardga,
    'Ice3':         Spell.Blizzardga,
    'Thunderga':    Spell.Thunderga,
    'Thundaga':     Spell.Thunderga,
    'Bolt3':        Spell.Thunderga,
    'Break':        Spell.Break,
    'Death':        Spell.Death,
    'Doom':         Spell.Death,
    'Holy':         Spell.Holy,
    'Pearl':        Spell.Holy,
    'Flare':        Spell.Flare,
    'Gravity':      Spell.Gravity,
    'Demi':         Spell.Gravity,
    'Gravityga':    Spell.Gravityga,
    'Quarter':      Spell.Gravityga,
    'Quartr':       Spell.Gravityga,
    'Dezone':       Spell.Dezone,
    'X-Zone':       Spell.Dezone,
    'Meteor':       Spell.Meteor,
    'Ultima':       Spell.Ultima,
    'Quake':        Spell.Quake,
    'Tornado':      Spell.Tornado,
    'WWind':        Spell.Tornado,
    'Meltdown':     Spell.Meltdown,
    'Merton':       Spell.Meltdown,
    'Library':      Spell.Library,
    'Libra':        Spell.Library,
    'Scan':         Spell.Library,
    'Slow':         Spell.Slow,
    'Rasp':         Spell.Rasp,
    'Silence':      Spell.Silence,
    'Mute':         Spell.Silence,
    'Protect':      Spell.Protect,
    'Safe':         Spell.Protect,
    'Sleep':        Spell.Sleep,
    'Confuse':      Spell.Confuse,
    'Muddle':       Spell.Confuse,
    'Haste':        Spell.Haste,
    'Stop':         Spell.Stop,
    'Berserk':      Spell.Berserk,
    'Bserk':        Spell.Berserk,
    'Float':        Spell.Float,
    'Kappa':        Spell.Kappa,
    'Imp':          Spell.Kappa,
    'Reflect':      Spell.Reflect,
    'Rflect':       Spell.Reflect,
    'Shell':        Spell.Shell,
    'Vanish':       Spell.Vanish,
    'Hastega':      Spell.Hastega,
    'Haste2':       Spell.Hastega,
    'Slowga':       Spell.Slowga,
    'Slow2':        Spell.Slowga,
    'Osmose':       Spell.Osmose,
    'Teleport':     Spell.Warp,
    'Warp':         Spell.Warp,
    'Quick':        Spell.Quick,
    'Dispel':       Spell.Dispel,
    'Cure':         Spell.Cure,
    'Curera':       Spell.Curera,
    'Cura':         Spell.Curera,
    'Cure2':        Spell.Curera,
    'Curega':       Spell.Curega,
    'Curaga':       Spell.Curega,
    'Cure3':        Spell.Curega,
    'Raise':        Spell.Raise,
    'Life':         Spell.Raise,
    'Arise':        Spell.Arise,
    'Araise':       Spell.Arise,
    'Life2':        Spell.Arise,
    'NullPoison':   Spell.NullPoison,
    'Poisona':      Spell.NullPoison,
    'Antdot':       Spell.NullPoison,
    'Antidote':     Spell.NullPoison,
    'NullStatus':   Spell.NullStatus,
    'Esuna':        Spell.NullStatus,
    'Remedy':       Spell.NullStatus,
    'Regen':        Spell.Regen,
    'Regenerate':   Spell.Regen,
    'Reraise':      Spell.Reraise,
    'Life3':        Spell.Reraise,
    'Flood':        Spell.Flood,
    'Gravityja':    Spell.Gravityja,
    'Gravija':      Spell.Gravityja,
    'Valor':        Spell.Valor
}

slots = defaultdict(lambda: 1)
slots[Spell.Ultima]     = 4
slots[Spell.Quick]      = 4
slots[Spell.Firega]     = 3
slots[Spell.Thunderga]  = 3
slots[Spell.Blizzardga] = 3
slots[Spell.Meltdown]   = 3
slots[Spell.Tornado]    = 3
slots[Spell.Quake]      = 3
slots[Spell.Arise]      = 3
slots[Spell.Curega]     = 3
slots[Spell.Hastega]    = 3
slots[Spell.Slowga]     = 3
slots[Spell.Osmose]     = 3
slots[Spell.Raise]      = 2
slots[Spell.Curera]     = 2
slots[Spell.Haste]      = 2
slots[Spell.Slow]       = 2

slots_gba = copy(slots)
slots_gba[Spell.Gravityja] = 3
slots_gba[Spell.Flood]     = 3
slots_gba[Spell.Valor]     = 3

class Esper(IntEnum):
    Ramuh         =  0
    Ifrit         =  1
    Shiva         =  2
    Siren         =  3
    Jormungand    =  4
    Catoblepas    =  5
    Maduin        =  6
    Bismarck      =  7
    CatSidhe      =  8
    Quetzali      =  9
    Valigarmander = 10
    Odin          = 11
    Raiden        = 12
    Bahamut       = 13
    Alexander     = 14
    Jihad         = 15
    Ragnarok      = 16
    QiLin         = 17
    ZonaSeeker    = 18
    Carbunkle     = 19
    Phantom       = 20
    Seraphim      = 21
    Golem         = 22
    Unicorn       = 23
    Fenrir        = 24
    Lakshmi       = 25
    Phoenix       = 26

    Leviathan = 27
    Cactender = 28
    Diabolus  = 29
    Gilgamesh = 30

    SNES_Count = 27
    GBA_Count = 31