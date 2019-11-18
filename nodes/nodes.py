# Abstract class for nodes used to build our tree
class Node():

    def __repr__(self):
        return self.options

    def __init__(self):
        # Subsequent nodes
        self.options = []
        # Pointer to the best node
        self.best = None
        # Best gain gotten from self.best.gain (absolute)
        self.gain = 0
        # Set this to True for root nodes (to jump from root to root)
        self.is_root = False
        # Next root node. Should be set only on leaves
        self.next = None

    # Browsing for the last node and returning its value
    def get_best_gain(self):
        if self.best is None:
            return self.gain
        return self.best.get_best_gain()

    # Function to override in power-related nodes
    def get_power_target(self):
        return self.best.get_power_target() if self.best is not None else None

    # Function to override in move-related nodes
    def get_move_target(self):
        return self.best.get_move_target() if self.best is not None else None

    def get_use_power(self):
        return self.best.use_power() if self.best is not None else 0

    def get_next_root_node(self):
        return self.next or self.get_next_root_node()