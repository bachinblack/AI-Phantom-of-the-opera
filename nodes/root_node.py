
from .character_nodes import DefaultChNode
from nodes import (
    nodes,
    # joseph_nodes as jn,
    # raoul_nodes as rn,
    # christine_nodes as cn,
    # persian_nodes as pn,
)


# For the given room id, the available passages
PASSAGES = [
    (1, 4), (0, 2), (1, 3), (2, 7), (0, 5, 8),
    (4, 6), (5, 7), (3, 6, 9), (4, 9), (7, 8)
]

# Available passages for pink character
PINK_PASSAGES = [
    (1, 4), (0, 2, 5, 7), (1, 3, 6), (2, 7), (0, 5, 8, 9),
    (4, 6, 1, 8), (5, 7, 2, 9), (3, 6, 9, 1), (4, 9, 5), (7, 8, 4, 6)
]


# The Root of our tree.
# It is called with a list of available characters.
# The leaves will call another root node with the remaining characters
# and so on until there is no character left.
class RootNode(nodes.Node):

    def __repr__(self):
        return (f"Root: {self.best}")

    def __init__(self, gamestate):

        self.is_root = True
        # Adding root node class in gamestate to call it from movenodes
        gamestate['root_node'] = RootNode
        # List of the characters and their predictions
        self.predictions = []
        # Best prediction
        self.best = None
        # All the implemented powers
        self.characters = {
            # "red": rn.RaoulNode,
            # "grey": jn.JosephNode,
            # "black": cn.ChristineNode,
            # "brown": pn.PersianNode,
        }

        for id, ch in enumerate(gamestate['options']):
            color = ch['color']
            # Getting the availables tiles to move to
            routes = PASSAGES[ch['position']] if color != 'pink' else PINK_PASSAGES[ch['position']]
            # If the lock is in one of the available paths, removing this path from the list
            if ch['position'] in gamestate['blocked']:
                # inspector_logger.warn(f"removing lock route {self.gamestate['blocked']}")
                routes = [r for r in routes if r not in gamestate['blocked']]
            try:
                # If the character was implemented, picking it
                # (pink doesn't need any implementation, just the pink_paths)
                tmp = self.characters[color](gamestate, color, routes)
            except KeyError:
                # Otherwise, using default CharacterNode
                tmp = DefaultChNode(gamestate, color, routes)
            tmp.options_index = id
            if self.best is None or abs(tmp.get_best_gain()) < abs(self.best.get_best_gain()):
                self.best = tmp
            self.predictions.append(tmp)
