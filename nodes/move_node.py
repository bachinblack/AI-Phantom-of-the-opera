
from copy import deepcopy as dcpy
from collections import defaultdict

from .nodes import Node
# from .root_node import RootNode
import display


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

        self.try_debug()
        if len(self.gamestate['options']) > 0:
            self.next = self.gamestate['root_node'](self.gamestate)

    def get_best_gain(self):
        return self.next.get_best_gain() if self.next is not None else self.gain

    def try_debug(self):
        # if display.debugger is not None:
        #     display.debugger.update(
        #         self.gamestate,
        #         self.gain,
        #         f"{self.character['color']}->{self.__repr__()}"
        #     )
        pass

    def get_move_target(self):
        return self.pos
