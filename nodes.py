from copy import deepcopy as dcpy
from collections import defaultdict

# The classes for our map of possibilities.
# it is possible to print them to see for every champion and every move
# What if the gain/loss


def get_rooms_list(gamestate: dict) -> dict:
    tmp = defaultdict(lambda: 0)
    # Sorting characters by room (removing non-suspects)
    for ch in gamestate['characters']:
        if ch['suspect']:
            tmp[ch['position']] += 1

    return tmp


# Returns the number of people isolated minus people grouped
# For the inspector, 0 is the best number. (positive > negative)
# For the ghost, 8 or -8 are the best (ghost being in the largest pool)
def compute_gain(gamestate: dict) -> int:
    rooms = defaultdict(lambda: 0)

    # Getting gain prediction
    total = 0
    for id, nb in get_rooms_list(gamestate).items():
        if nb == 1 or id == gamestate['shadow']:
            # isolated people are negative
            total -= nb
        else:
            # grouped people are positive
            total += nb
    return total


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
        print(self.__repr__())
        return self.best.get_move_target() if self.best is not None else None


# Stores an array of MoveNodes from all the available moves
# Get all the gains from the moves and tell wich one's best
class CharacterNode(Node):

    def __repr__(self):
        return f"{self.character['color']}: {self.options} >>{self.best}<<"

    def __init__(self, gamestate, character, moves):
        Node.__init__(self)
        self.character = character
        self.is_root = True

        # get character index
        for id, c in enumerate(gamestate['characters']):
            if c['color'] == character:
                break

        for m in moves:
            tmp = MoveNode(gamestate, id, m)
            # Keeping track of the closest value to 0
            if self.best is None or abs(tmp.gain) < abs(self.best.gain):
                self.best = tmp
                self.gain = abs(tmp.gain)
            self.options.append(tmp)


# Raoul (red) gets to draw an alibi card
class RaoulNode(CharacterNode):

    def __repr__(self):
        return f"Raoul: {self.options} >>{self.best+0.5}<<"

    def __init__(self, gamestate, character, moves):
        CharacterNode.__init__(self, gamestate, character, moves)
        # There is a probability to get an alibi on a character
        # Always use his power
        self.power = 1

    # Browsing for the last node and returning its value
    def get_best_gain(self):
        # Adding only .5 to this score, as +1 gain is not guaranted
        return self.best.get_best_gain() + 0.5


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
        # At equal gain, it is better to pick the one where people are grouped
        if self.gain > 0:
            self.gain += 0.1

    def get_move_target(self):
        return self.pos
