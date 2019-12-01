#!/usr/bin/python3.6
from player import Player
from compute_gain import (
    inspector_gain as holmes,
    inspector_ghost_gain as moriarty
)


class Inspector(Player):

    def __init__(self):
        # The intent of the AI for the given and subsequent moves.
        # The key corresponds to the number of options during the move.
        # We can simply pass it to the roots.
        # They will pop and call elements from it.
        self.intents = {
            4: [holmes, moriarty, moriarty, holmes],
            3: [holmes, holmes, moriarty],
            2: [holmes, moriarty],
            1: [holmes]
        }

        Player.__init__(self)


if __name__ == "__main__":
    p = Inspector()
    p.run()
