from copy import deepcopy as dcpy
from collections import defaultdict
import display


# The classes for our map of possibilities.
# They are printable for clarity.
def get_rooms_list(gamestate: dict) -> dict:
    # The first element is the total number and the second is the number of suspects
    tmp = defaultdict(lambda: [0, 0])
    # Sorting characters by room (removing non-suspects)
    for ch in gamestate['characters']:
        tmp[ch['position']][0] += 1
        if ch['suspect']:
            tmp[ch['position']][1] += 1

    return tmp


# Returns the number of people isolated minus people grouped
# For the inspector, 0 is the best number. (positive > negative)
# For the ghost, 8 or -8 are the best (ghost being in the largest pool)
def compute_gain(gamestate: dict) -> int:
    rooms = defaultdict(lambda: 0)

    # Getting gain prediction
    total = 0
    for id, nbs in get_rooms_list(gamestate).items():
        if nbs[0] == 1 or id == gamestate['shadow']:
            # isolated people are negative
            total -= nbs[1]
        else:
            # grouped people are positive
            total += nbs[1]
    return total


# Abstract class for nodes used to build our tree
class Node():

    def __repr__(self):
        return self.options

    def __init__(self):
        # Subsequent nodes
        self.options = []
        # Pointer to the best node
        self.best = None
        # Best gain gotten from self.best.gain (absolute)
        self.gain = 0
        # Whether or not to use its power
        self.power = 0
        # Set this to True for character nodes (to jump from root to root)
        self.is_root = False

    # Browsing for the last node and returning its value
    def get_best_gain(self):
        if self.best is None:
            return self.gain
        return self.best.get_best_gain()

    # Function to override in power-related nodes
    def get_power_target(self):
        return self.best.get_power_target() if self.best is not None else None

    # Function to override in move-related nodes
    def get_move_target(self):
        return self.best.get_move_target() if self.best is not None else None

    def get_use_power(self):
        return self.best.use_power() if not use_power else use_power


# Calculates the state of the game for a given character's new position
# Returns a gain to it's CharacterNode
class MoveNode(Node):

    def __repr__(self):
        return (f"Move->{self.pos}: {self.gain}")

    def __init__(self, gamestate: dict, charid: int, pos: int):
        Node.__init__(self)

        # Copy the state of the game, then set the original inaccessible
        self.gamestate = dcpy(gamestate)
        gamestate = None

        self.pos = pos

        self.character = self.gamestate['characters'][charid]
        self.character['position'] = self.pos
        self.gain = compute_gain(self.gamestate)

        self.try_debug()

    def try_debug(self):
        if display.debugger is not None:
            display.debugger.update(
                self.gamestate,
                self.gain,
                f"{self.character['color']}->{self.__repr__()}"
            )

    def get_move_target(self):
        return self.pos
