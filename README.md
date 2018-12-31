# Asura

Asura is a program for generating a 'four esper' challenge run for Final Fantasy 6. Only the US releases for the Super Nintendo and all official releases for the Game Boy Advance are supported.

Asura is copyrighted under the [GNU Affero General Public License, version 3](https://www.gnu.org/licenses/agpl-3.0.en.html).

## Usage

> `./main.py rom.ext [seed|None[ A,List,Of,Spells]]`

`rom.ext` must be a ROM image of Final Fantasy III for the SNES (either revision) or Final Fantasy VI Advance (Japanese, US, or European releases).

`seed`, if passed and not 'None', uses the time as of the running of the script for the seed.

The final argument is a list of spells to prohibit. All official spell names are recognized.

## Notes

The spell selection mechanism uses two separate kinds of slots. The game itself supports up to five spells per esper, but for balance purposes each spell costs a number of points in the range [1,5], and each esper has 6 points to 'spend'. The following table enumerates the *current* point assignments (spells not enumerated cost one point):

<table>
    <thead>
        <tr><th>Spell</th><th>Pts</th><th>Spell</th><th>Pts</th><th>Spell</th><th>Pts</th><th>Spell</th><th>Pts</th></tr>
    </thead>
    <tbody>
        <tr><td>Quick</td><td align="center">5</td>
            <td>Arise</td><td align="center">4</td>
            <td>Death</td><td align="center">3</td>
            <td>Cura</td><td align="center">2</td></tr>
        <tr><td>Ultima</td><td align="center">5</td>
            <td>Blizzaga</td><td align="center">4</td>
            <td>Graviga</td><td align="center">3</td>
            <td>Haste</td><td align="center">2</td></tr>
        <tr><td>Gravija</td><td align="center">5</td>
            <td>Curaga</td><td align="center">4</td>
            <td>Hastega</td><td align="center">3</td>
            <td>Raise</td><td align="center">2</td></tr>
        <tr><td colspan="2"></td>
            <td>Firaga</td><td align="center">4</td>
            <td>Esuna</td><td align="center">3</td>
            <td>Reraise</td><td align="center">2</td></tr>
        <tr><td colspan="2"></td>
            <td>Meltdown</td><td align="center">4</td>
            <td>Osmose</td><td align="center">3</td>
            <td>Slow</td><td align="center">2</td></tr>
        <tr><td colspan="2"></td>
            <td>Quake</td><td align="center">4</td>
            <td colspan="4"></td></tr>
        <tr><td colspan="2"></td>
            <td>Slowga</td><td align="center">4</td>
            <td colspan="4"></td></tr>
        <tr><td colspan="2"></td>
            <td>Thundaga</td><td align="center">4</td>
            <td colspan="4"></td></tr>
        <tr><td colspan="2"></td>
            <td>Tornado</td><td align="center">4</td>
            <td colspan="4"></td></tr>
        <tr><td colspan="2"></td>
            <td>Flood</td><td align="center">4</td>
            <td colspan="4"></td></tr>
        <tr><td colspan="2"></td>
            <td>Valor</td><td align="center">4</td>
            <td colspan="4"></td></tr>
    </tbody>
</table>
