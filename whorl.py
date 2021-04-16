#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class WorldItem:
    name: str
    desc: str

    def describe(self):
        print("""{}
        {}""".format(self.name, self.desc))


class Direction:
    def __init__(self, name, complement=None):
        self.name = name
        self.complement = complement

    def set_complement(self, comp):
        self.complement = comp

class Environment:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.stuff = {'self': self}
        self.description_string = """{}

{}
---
Contents:
"""
        self.exits = {}

    def has(obj):
        return obj in self.stuff

    def describe(self):
        print(self.description_string.format(self.name, self.desc))

        for name, item in self.stuff.items():
            if name == 'self':
                continue

            item.describe()
            print()

    def add_stuff(self, more_stuff):
        if 'self' in more_stuff:
            del more_stuff['self']
        self.stuff = {**self.stuff, **more_stuff}

    def door(self, dir, goes_to, one_way=False):
        self.exits[dir] = goes_to

        if not one_way:
            goes_to.door(dir.complement, self, one_way=True)

    def __getitem__(self, k):
        return self.stuff[k]

    def has_exit(self, dir):
        return dir in self.exits

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 10
        self.attrs = {
            'strength': 0,
            'dexterity': 0,
            'constitution': 0,
            'intelligence': 0,
            'wisdom': 0,
            'charisma': 0,
        }
        self.env = None

    def load(name):
        return db.get_player(name)

    def inside(self, e):
        self.env = e


# This is a one line comment
"""
This is a multiline comment
"""
class Whorl:
    def __init__(self, directions):
        self._player = None
        self._dirmap = directions

    def _input(self):
        inputtokens = input('> ').split(' ')
        return (inputtokens[0], inputtokens[1:])

    def play(self, _as=None):
        self._player = _as
        cmd, args = self._input()

        while cmd != 'q':
            if cmd == '':
                cmd, args = self._input()
                continue

            fn = getattr(self, cmd)
            fn(*args)
            cmd, args = self._input()

    def look(self, *args):
        at = 'self'
        if args:
            at = args[0]

        self._player.env[at].describe()

    def go(self, dirname):
        room = self._player.env
        dir = self._dirmap[dirname]
        if room.has_exit(dir):
            self._player.inside(room.exits[dir])


## Directions
## --------------------------------------------------
north = Direction('north')
south = Direction('south')
east = Direction('west')
west = Direction('west')

north.set_complement(south)
south.set_complement(north)
east.set_complement(west)
west.set_complement(east)

## Rooms
## --------------------------------------------------
StudioApt = Environment('Apt. 311', """
The 11th apartment on the third floor.""")
StudioApt.add_stuff({
    'couch': WorldItem('Couch', 'A large grey sectional with three sides.'),
    'table': WorldItem('Coffee Table', 'Matte black and stationed between two sides of the couch.')
})

Hallway = Environment('3rd floor hallway', """
The 3rd floor hallway of Mia luxury apartments""")


StudioApt.door(south, Hallway)


matt = Player('matt')
matt.inside(StudioApt)


whorl_directions = {
    'north': north,
    'south': south,
    'east': east,
    'west': west,
}

game = Whorl(directions=whorl_directions)

game.play(_as=matt)
