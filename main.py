#!/usr/bin/env python3

from sys import argv, exit
from time import time

import os.path as op

from asura import generate, write_rom, write_spoilers
from asura.data import spell_map

if len(argv) < 2 or len(argv) > 4:
    print('Usage: {} <filename> [seed [forbidden,spells,...]]'.format(argv[0]))
    exit(1)

if len(argv) == 2 or (len(argv) >= 3 and argv[2] == 'None'):
    seed = str(time()).split('.')[0]
if len(argv) >= 3:
    seed = argv[2] if argv[2] 
if len(argv) == 4:
    spells = argv[3].split(',')
    forbidden = [spell_map[i] for i in spells]
else:
    forbidden = []

filename = argv[1]
namebase, ext = op.splitext(filename)
ext = ext[1:]
output_rom = '.'.join([namebase, seed, ext])
output_txt = '.'.join([namebase, seed, 'txt'])

mode = 'snes' if ext != 'gba' else 'gba'

espers = generate(seed, mode, forbidden)

print('Seed: {}\n'.format(seed))
print('Writing ROM...')
write_rom(filename, output_rom, mode, espers)
print('Writing spoilers...')
write_spoilers(output_txt, espers, seed)
