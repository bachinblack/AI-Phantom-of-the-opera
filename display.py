from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.image as mpimg
from collections import defaultdict


# This is where the debugger will live.
def init_debug(graph: bool):
    global debugger
    debugger = Display() if graph else None


class Display():

    def __init__(self):
        self.img = mpimg.imread('res/board.png')
        _, self.ax = plt.subplots(1)

        self.ax.imshow(self.img)
        plt.ion()
        plt.show()

        # The top-left position of each room
        self.rooms = [
            (1350, 550),
            (1010, 560),
            (700, 560),
            (260, 540),

            (1330, 365),
            (1000, 380),
            (610, 350),
            (280, 300),

            (970, 160),
            (640, 175)
        ]

        # Available positions inside a room
        self.positions = [
            (0, 0),
            (30, 0),
            (60, 0),

            (0, 30),
            (30, 30),
            (60, 30),

            (15, 60),
            (45, 60),
        ]

    def update(self, gamestate, gain, note):
        dd = defaultdict(lambda: 0)
        self.ax.clear()
        self.ax.imshow(self.img)

        # Displaying characters (as circles)
        for ch in gamestate['characters']:
            pos = ch['position']
            room = self.rooms[pos]
            fpos = tuple(map(sum, zip(room, self.positions[dd[pos]])))
            if ch['suspect']:
                p = Circle(fpos, 20, color=ch['color'])
            else:
                p = Rectangle(fpos, 20, 20)
            self.ax.add_patch(p)
            dd[pos] += 1

        # Displaying text (gain, shadow, lock and note)
        plt.text(5, -15, "Gain = " + str(gain))
        plt.text(5, -35, "Shadow = " + str(gamestate['shadow']))
        plt.text(5, -55, "Lock = " + str(gamestate['blocked']))
        plt.text(5, -75, note)

        # Drawing and waiting for an input
        plt.draw()
        plt.pause(0.001)
        input("Press [enter] to continue.")
