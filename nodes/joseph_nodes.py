from copy import deepcopy as dcpy
from .nodes import Node
from .move_node import MoveNode
from .character_nodes import CharacterNode


# Joseph (grey) can move the blackout.
# He will try it in every room for every room he can go.
class JosephNode(CharacterNode):

    def __repr__(self):
        return f"Joseph: {self.best}"

    def __init__(self, gamestate: dict, chcol: str, moves: list):
        CharacterNode.__init__(self, gamestate, chcol)
        gamestate = None

        # Use the power for every room
        for room in range(10):
            tmp = BlackoutNode(self.gamestate, room, self.id, moves)
            self.update_best_node(tmp)
            self.options.append(tmp)

    def get_power_target(self):
        print("get best power target")
        return self.best.get_power_target() if self.best is not None else None


class BlackoutNode(Node):

    def __repr__(self):
        return (f"Blackout->{self.pos}: {self.best}")

    def __init__(self, gamestate: dict, room: int, charid: int, moves: list):
        Node.__init__(self)

        # Copy the state of the game then remove original to avoid using it
        self.gamestate = dcpy(gamestate)
        gamestate = None

        self.pos = room

        # Moving the blackout to the given room
        self.gamestate['shadow'] = room

        # Check every possible move
        for m in moves:
            tmp = MoveNode(self.gamestate, charid, m)
            self.update_best_node(tmp)
            self.options.append(tmp)

    # Keeping track of the highest value
    def update_best_node(self, tmp):
        if self.best is None or tmp.gain > self.best.gain:
            self.best = tmp
            self.gain = tmp.gain

    # Function to override in power-related nodes
    def get_power_target(self):
        print(f"Grey power target: {self.pos}")
        return self.pos
