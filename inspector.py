#!/usr/bin/python3.6
from player import Player

class Inspector(Player):

    def __init__(self):
        Player.__init__(self)

        # The intent of the AI for the given and subsequent moves.
        # key: The number of options available
        # True: Intent to ensure dichotomy. (inspector's turn)
        # False: Intent to avoid it AND hide the ghost. (fantom's turn)
        # Basically, the intent depends on who will play the move.
        self.intent = {
            4: [True, False, False, True],
            3: [True, True, False],
            2: [True, False],
            1: [True]
        }

        # The inspector doesn't know who the ghost is.
        self.ghost = None

if __name__ == "__main__":
    p = Inspector()
    p.run()
