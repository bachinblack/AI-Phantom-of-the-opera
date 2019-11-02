from copy import deepcopy as dcpy
from nodes import Node, MoveNode


class JosephNode(Node):

    def __repr__(self):
        return f"Joseph: {self.options} >>{self.best}<<"

    def __init__(self, gamestate: dict, character: dict, moves: list):
        print("Joseph node")
        Node.__init__(self)

        # get character index
        for id, c in enumerate(gamestate['characters']):
            if c['color'] == 'grey':
                break

        # Use the power for every room
        for room in range(10):
            tmp = BlackoutNode(gamestate, room, id, moves)
            # Keeping track of the closest value to 0
            if self.best is None or abs(tmp.gain) < abs(self.best.gain):
                self.best = tmp
                self.gain = tmp.gain
            self.options.append(tmp)


class BlackoutNode(Node):

    def __repr__(self):
        return (f"Blackout->{self.pos}: {self.options}")

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
            # Keeping track of the closest value to 0
            if self.best is None or abs(tmp.gain) < abs(self.best.gain):
                self.best = tmp
                self.gain = tmp.gain
            self.options.append(tmp)

    # Function to override in power-related nodes
    def get_power_target(self):
        return self.pos
