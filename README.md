# Asura

Asura is a program for generating a 'four esper' challenge run for Final Fantasy 6. Only the US releases for the Super Nintendo and all official releases for the Game Boy Advance are supported.

Asura is made available under the terms of the MIT license; see `COPYING` for more information.

## Requirements

* Python 3.4+
* A US release of Final Fantasy III for the Super Nintendo OR any official Game Boy Advance release of Final Fantasy VI.

## Usage

> `./main.py rom.ext [seed|None[ A,List,Of,Spells]]`

`rom.ext` must be a ROM image of Final Fantasy III for the SNES (either revision) or Final Fantasy VI Advance (Japanese, US, or European releases).

`seed`, if passed and not 'None', uses the time as of the running of the script for the seed.

The final argument is a list of spells to prohibit. All official spell names are recognized.

## Notes

The spell selection mechanism uses two separate kinds of slots. The game itself supports up to five spells per esper, but for balance purposes each spell costs a number of points in the range [1,5], and each esper has 6 points to 'spend'. The following table enumerates the *current* point assignments (spells not enumerated cost one point):

| Spell   | Pts | Spell    | Pts | Spell   | Pts | Spell   | Pts |
| ------- | --- | -------- | --- | ------- | --- | ------- | --- |
| Quick   |  5  | Arise    |  4  | Death   |  3  | Cura    |  2  |
| Ultima  |  5  | Blizzaga |  4  | Graviga |  3  | Haste   |  2  |
| Gravija |  5  | Curaga   |  4  | Hastega |  3  | Raise   |  2  |
|         |     | Firaga   |  4  | Esuna   |  3  | Reraise |  2  |
|         |     | Meltdown |  4  | Osmose  |  3  | Slow    |  2  |
|         |     | Quake    |  4  |
|         |     | Slowga   |  4  |
|         |     | Thundaga |  4  |
|         |     | Tornado  |  4  |
|         |     | Flood    |  4  |
|         |     | Valor    |  4  |

## Special Thanks

The following people contributed to this project:

* Lenophis: Provided the esper-gain offsets for the SNES US release.
* [ff6hacking.com](https://ff6hacking.com): Provided the esper data offsets and lists.
* Can of Worms: Figured out the esper-gain offsets for the GBA releases, including the bonus content espers.
