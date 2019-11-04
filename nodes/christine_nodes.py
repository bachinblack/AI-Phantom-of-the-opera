from copy import deepcopy as dcpy
from .nodes import Node, CharacterNode, MoveNode, compute_gain


class ChristineNode(CharacterNode):

    def __repr__(self):
        return f"Christine: {self.options} >>{self.best}<<"

    def __init__(self, gamestate: dict, chcol: str, moves: list):
        Node.__init__(self)

        # getting character index
        id, _ = self.get_character_id(gamestate['characters'], chcol)
        # for id, c in enumerate(gamestate['characters']):
        #     if c['color'] == 'black':
        #         break

        for m in moves:
            # Without power
            tmp = MoveNode(gamestate, id, m)
            # Keeping track of the closest value to 0
            if self.best is None or abs(tmp.gain) < abs(self.gain):
                self.best = tmp
                self.gain = tmp.gain
            self.options.append(tmp)

            # With power (need to know which rooms are accessible from new pos)
            # tmp = ChristineMoveNode(gamestate, id, m)
            # # Keeping track of the closest value to 0
            # if abs(tmp.gain) < abs(self.gain):
            #     self.best = tmp
            #     self.gain = tmp.gain
            # self.options.append(tmp)


# Move christine to the given location, calculate gain,
# then use power and recalculate gain
class ChristineMoveNode(MoveNode):

    def __repr__(self):
        return (f"ChristineMove->{self.pos}: {self.gain}")

    def __init__(self, gamestate: dict, charid: int, pos: int, moves: list):
        Node.__init__(self)

        # Copy the state of the game, then set the original inaccessible
        self.gamestate = dcpy(gamestate)
        gamestate = None

        self.pos = pos

        print("-----  CHR  -----")
        print(self.pos)

        # Drawing everyone around to the given room (including christine)
        for ch in self.gamestate['characters']:
            if ch['position'] in moves:
                ch['position'] = self.pos
                print(ch['color'])

        print("-----------------")

        self.gain = compute_gain(self.gamestate)
