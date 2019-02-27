# Python 3.7
import pygame
import time
import random

CELL_OUTER_RATE = 0;  # This is the speed that the outer (colour) value is changed by.
CELL_INNNER_RATE = 0;  # This is the speed that the stored value is changed by.

WORLD_SIZE = 64
VAL_RANGE = 180
CELL_APPEARANCE = 64  # Smaller means more cells.

# Cells are formatted: (hsv-outer, hsv-innner)
# -1 in the first slot means that there is no cell there: (-1, hue)
g_cell_matrix = []

def init():
    global g_cell_matrix

    random.seed()  # Init rng

    # Create 64x64 matrix of tuples.
    g_cell_matrix = [[
        (random.randint(0, VAL_RANGE) if random.randint(0, CELL_APPEARANCE) == 0 else -1, 0)
        for y in range(0, WORLD_SIZE)]
        for x in range(0, WORLD_SIZE)]

g_exit = False
# Update simulation.
def update():
    global g_exit

    #while not g_exit:
        #pass
        #time.sleep(1000/60);

# Call functions after file guard.
if __name__ == "__main__":
    init()
    update()

    pause = input("program ended")
