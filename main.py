#!/usr/bin/env python3
# Copyright 2023 Síle Ekaterin Liszka
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
