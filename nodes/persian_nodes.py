from copy import deepcopy as dcpy
from .nodes import Node
from .move_node import MoveNode, compute_gain
from .character_nodes import CharacterNode


# The persian (brown) can take someone with him.
# He'll try it with every people in the room for every room he can go to.
class PersianNode(CharacterNode):

    def __repr__(self):
        return f"Persian: {self.best}"

    def __init__(self, gamestate: dict, chcol: str, moves: list):
        CharacterNode.__init__(self, gamestate, chcol)

        targets = self.get_people_in_room(self.character['position'])

        for m in moves:
            # Without power
            tmp = MoveNode(self.gamestate, self.id, m)
            # Keeping track of the closest value to 0
            if self.best is None or abs(tmp.gain) < abs(self.gain):
                self.best = tmp
                self.gain = tmp.gain
            self.options.append(tmp)

            # With power
            # Trying to move with each people in the room
            for t in targets:
                tmp = PersianMoveNode(self.gamestate, self.id, m, t)
                # Keeping track of the closest value to 0
                if abs(tmp.gain) < abs(self.gain):
                    self.best = tmp
                    self.gain = tmp.gain
                self.options.append(tmp)

    def get_people_in_room(self, room):
        return [id for id, ch in enumerate(self.gamestate['characters']) if ch['position'] == room and ch['color'] != 'brown']


class PersianMoveNode(MoveNode):

    def __repr__(self):
        return (f"PersianMove->{self.pos}: {self.gain}")

    def __init__(self, gamestate: dict, charid: int, pos: int, targetid: int):
        Node.__init__(self)

        # Copy the state of the game, then set the original inaccessible
        self.gamestate = dcpy(gamestate)
        gamestate = None

        self.pos = pos
        self.character = {'color': 'brown'}

        # Moving the persian and one other character to the next room
        self.gamestate['characters'][charid]['position'] = pos
        self.gamestate['characters'][targetid]['position'] = pos

        self.gain = compute_gain(self.gamestate)
        self.try_debug()

    def get_use_power(self):
        # We're in a power node, so we always use the power
        return 1