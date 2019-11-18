#!/usr/bin/python3.6
from player import Player

class Fantom(Player):

    def __init__(self):
        Player.__init__(self)

        # The intent of the AI for the given and subsequent moves.
        # key: The number of options available
        # True: Intent to ensure dichotomy. (inspector's turn)
        # False: Intent to avoid it AND hide the ghost. (fantom's turn)
        # Basically, the intent depends on who will play the move.
        self.intent = {
            4: [False, True, True, False],
            3: [False, False, True],
            2: [False, True],
            1: [False]
        }

        # The ghost knows who the ghost is and plays around this
        self.ghost = None


if __name__ == "__main__":
    p = Fantom()
    p.run()
