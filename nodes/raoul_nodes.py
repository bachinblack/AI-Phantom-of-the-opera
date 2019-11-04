from .nodes import CharacterNode


# Raoul (red) gets to draw an alibi card
class RaoulNode(CharacterNode):

    def __repr__(self):
        return f"Raoul: {self.options} >>{self.best}+0.5<<"

    def __init__(self, gamestate, character, moves):
        CharacterNode.__init__(self, gamestate, character, moves)
        # There is a probability to get an alibi on a character
        # Always use his power
        self.power = 1

    # Browsing for the last node and returning its value
    def get_best_gain(self):
        # Adding only .5 to this score, as +1 gain is not guaranted
        return self.best.get_best_gain() + 0.5
