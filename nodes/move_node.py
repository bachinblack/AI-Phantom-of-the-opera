
from copy import deepcopy as dcpy
from collections import defaultdict

from .nodes import Node
# from .root_node import RootNode
import display


# def get_rooms_list(gamestate: dict) -> dict:
#     # The first element is the total number and the second is the number of suspects
#     tmp = defaultdict(lambda: [0, 0])
#     # Sorting characters by room (removing non-suspects)
#     for ch in gamestate['characters']:
#         tmp[ch['position']][0] += 1
#         if ch['suspect']:
#             tmp[ch['position']][1] += 1

#     return tmp


# Returns the number of people isolated minus people grouped
# For the inspector, 0 is the best number. (positive > negative)
# For the ghost, 8 or -8 are the best (ghost being in the largest pool)
# def compute_gain(gamestate: dict) -> int:
#     total = 0
#     for id, nbs in get_rooms_list(gamestate).items():
#         if nbs[0] == 1 or id == gamestate['shadow']:
#             # isolated people are negative
#             total -= nbs[1]
#         else:
#             # grouped people are positive
#             total += nbs[1]
#     return total


# Calculates the state of the game for a given character's new position
# Returns a gain to it's CharacterNode
class MoveNode(Node):

    def __repr__(self):
        if self.next is not None:
            return (f"Move->{self.pos}: {self.gain} | next: {self.next.best}")
        return (f"Move->{self.pos}: {self.gain}")

    def __init__(self, gamestate: dict, charid: int, pos: int):
        Node.__init__(self)

        # Copy the state of the game, then set the original inaccessible
        self.gamestate = dcpy(gamestate)
        gamestate = None

        self.pos = pos

        self.character = self.gamestate['characters'][charid]
        self.character['position'] = self.pos
        self.gain = self.gamestate['compute_gain'].pop(0)(self.gamestate)

        # self.try_debug()
        if len(self.gamestate['options']) > 0:
            self.next = self.gamestate['root_node'](self.gamestate)

    def try_debug(self):
        if display.debugger is not None:
            display.debugger.update(
                self.gamestate,
                self.gain,
                f"{self.character['color']}->{self.__repr__()}"
            )

    def get_move_target(self):
        return self.pos
