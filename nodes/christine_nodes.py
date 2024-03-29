from copy import deepcopy as dcpy
from .nodes import Node
from .move_node import MoveNode
from .character_nodes import CharacterNode


# Christine (black) can draw everyone in her room.
# She will try it in every room she can go
class ChristineNode(CharacterNode):

    def __repr__(self):
        return f"Christine: {self.best}"

    def __init__(self, gamestate: dict, chcol: str, moves: list):
        CharacterNode.__init__(self, gamestate, chcol)

        # For the given room id, the available passages
        self.passages = [
            (1, 4), (0, 2), (1, 3), (2, 7), (0, 5, 8),
            (4, 6), (5, 7), (3, 6, 9), (4, 9), (7, 8)
        ]

        for m in moves:
            # Without power
            tmp = MoveNode(self.gamestate, self.id, m)
            # Keeping track of the closest value to 0
            self.update_best_node(tmp)
            self.options.append(tmp)

            # With power
            tmp = ChristineMoveNode(self.gamestate, self.id, m, self.passages[m])
            # Keeping track of the closest value to 0
            self.update_best_node(tmp)
            self.options.append(tmp)


class ChristineMoveNode(MoveNode):

    def __repr__(self):
        return f"{MoveNode.__repr__(self)} (power)"

    def __init__(self, gamestate: dict, charid: int, pos: int, moves: list):
        Node.__init__(self)

        # Copy the state of the game, then set the original inaccessible
        self.gamestate = dcpy(gamestate)
        gamestate = None

        self.pos = pos
        self.character = {'color': 'Christine'}

        # Drawing everyone around to the given room (including christine)
        for ch in self.gamestate['characters']:
            if ch['position'] in moves:
                ch['position'] = self.pos

        self.gain = self.gamestate['compute_gain'].pop(0)(self.gamestate)
        self.try_debug()

        if len(self.gamestate['options']) > 0:
            self.next = self.gamestate['root_node'](self.gamestate)

    def get_use_power(self):
        # We're in a power node, so we always use the power
        return 1