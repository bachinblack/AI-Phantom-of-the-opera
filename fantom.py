#!/usr/bin/python3.6
from player import Player
from compute_gain import (
    ghost_gain as moriarty,
    inspector_gain as holmes
)


class Fantom(Player):

    def __init__(self):
        # The intent of the AI for the given and subsequent moves.
        # The key corresponds to the number of options during the move.
        # We can simply pass it to the roots.
        # They will pop and call elements from it.
        self.intents = {
            4: [moriarty, holmes, holmes, moriarty],
            3: [moriarty, moriarty, holmes],
            2: [moriarty, holmes],
            1: [moriarty]
        }

        Player.__init__(self)


if __name__ == "__main__":
    p = Fantom()
    p.run()
