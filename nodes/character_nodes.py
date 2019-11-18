from copy import deepcopy as dcpy

from .nodes import Node
from .move_node import MoveNode

# The abstract class "CharacterNode"
class CharacterNode(Node):

    def __init__(self, gamestate, chcol: str):
        Node.__init__(self)
        self.is_root = True

        self.gamestate = dcpy(gamestate)

        # get character index
        self.id, self.character = self.get_character_id(
            self.gamestate['characters'],
            chcol
        )

        # Removing current character from options.
        self.gamestate['options'].pop(
            next(id for id, ch in enumerate(self.gamestate['options']) if ch['color'] == chcol)
        )

    def get_character_id(self, characters: list, chcol: str) -> tuple:
        for id, c in enumerate(characters):
            if c['color'] == chcol:
                return (id, c)
        return (-1, None)


# Default character class used for not yet defined characters
class DefaultChNode(CharacterNode):

    def __repr__(self):
        return f"{self.character['color']}: {self.options} >>{self.best}<<"

    def __init__(self, gamestate: object, chcol: str, moves: list):
        CharacterNode.__init__(self, gamestate, chcol)

        for m in moves:
            tmp = MoveNode(self.gamestate, self.id, m)
            # Keeping track of the closest value to 0
            if self.best is None or abs(tmp.gain) < abs(self.best.gain):
                self.best = tmp
                self.gain = abs(tmp.gain)
            self.options.append(tmp)

    def get_use_power(self):
        # For default characters, never use power
        return 0