# Python 3.7
import pygame
import time
import random

# Setup Constants
SCREEN_SIZE = [1024, 768]
FPS = 30

# Call functions after file guard.
if __name__ == "__main__":
    # Starts and sets up pygame
    pygame.init()
    DISPLAY_SURFACE = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Father, what is my name?!")

# Runtime Constants
dt = 0
game_stopped = False

# Application Constants
CELL_OUTER_RATE = 0.4/4;  #0.4 This is the speed that the outer (colour) value is changed by.
CELL_INNNER_RATE = 0.7/2;  #0.7 This is the speed that the stored value is changed by.  0.3 == 30% average.

WORLD_SIZE = 64  # Is width & height.
CELL_SIZE = 8  # Is width & height.
CELL_APPEARANCE = 0  # Smaller means more cells.
VAL_RANGE = 359

# Cells are formatted: (hsv-outer, hsv-innner)
# -1 in the first slot means that there is no cell there: (-1, hue)
g_cell_array = []

def init():
    global g_cell_array

    random.seed()  # Init rng

    # Create 64*64 array of tuples. (a folded matrix)
    g_cell_array = [
        (random.randint(0, VAL_RANGE) if random.randint(0, CELL_APPEARANCE) == 0 else -1, 0)
        for n in range(0, WORLD_SIZE**2)]

# This function handles any input.  Called before draw.
def handle_input():
    global game_stopped
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_stopped = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                init()

# This is for drawing stuff.  Called before update.
def draw():
    global g_cell_array

    for i in range(0, len(g_cell_array)):
        r = pygame.Rect(i%WORLD_SIZE*CELL_SIZE, i//WORLD_SIZE*CELL_SIZE, CELL_SIZE, CELL_SIZE)

        if g_cell_array[i][0] != -1:
            c = pygame.Color(0, 0, 0, 0)
            c.hsva = (g_cell_array[i][0], 100, 100, 100)
            pygame.draw.rect(DISPLAY_SURFACE, c, r)
        else:
            pygame.draw.rect(DISPLAY_SURFACE, (0, 0, 0), r)  # Draws Black Box

# This is the "do game math" function.
def update():
    global g_cell_array
    print(g_cell_array[12])
    # Make a temp copy of the array to take values from.
    cell_array_cpy = g_cell_array.copy()

    # Iterate all cells and do operations on them.
    for i in range(0, len(g_cell_array)):
        if cell_array_cpy[i][0] != -1:
            new_val = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x!=0) and (y!=0) :
                        key = i+x+y*WORLD_SIZE
                        if x%WORLD_SIZE == WORLD_SIZE-1:
                            key -= (WORLD_SIZE-1)
                        if y == 1 and i//WORLD_SIZE == WORLD_SIZE-1:
                            key -= WORLD_SIZE**2
                        if x == 1 and i%WORLD_SIZE == WORLD_SIZE-1:
                            key -= 2
                        new_val += cell_array_cpy[key][0]

            new_inner_val = cell_array_cpy[i][1]*(1-CELL_INNNER_RATE) + CELL_INNNER_RATE*new_val/4
            new_outer_val = cell_array_cpy[i][0]*(1-CELL_OUTER_RATE) + new_inner_val*CELL_OUTER_RATE
            #g_cell_array[i] = (new_outer_val if new_outer_val < VAL_RANGE else new_outer_val - VAL_RANGE,
            #                    new_inner_val if new_inner_val < VAL_RANGE else new_inner_val - VAL_RANGE)
            g_cell_array[i] = (new_outer_val, new_inner_val)


# This is the gameloop section of code.
def gameloop():
    global dt

    # This is the start of the gameloop.
    while not game_stopped:
        fs = pygame.time.get_ticks()  # Get time before calulations.

        handle_input()  # First Gameloop Stage.
        update()  # Second Gameloop Stage.
        draw() # Last Gameloop Stage.

        pygame.display.update() # Updates the display with changes.

        # wait_time = time_single_frame - time_elapsed
        wait_time = ((1/float(FPS))*1000) - (pygame.time.get_ticks()-fs)
        #print( "DEBUG: frame_lag = " + str((1/float(FPS))*1000) + " .. " + str((pygame.time.get_ticks()-fs)) )

        pygame.time.wait(int(wait_time))  # Pause the program for the set amount of time.

        # This updates the delta time variable. (in seconds, not ms)
        dt = ( wait_time + (pygame.time.get_ticks() - fs) ) / 1000.0
        #print( "DEBUG: dt = " + str(dt) )

    pygame.quit()  # Close pygame before application closes.

# Call functions after file guard.
if __name__ == "__main__":
    init()
    gameloop()

    pause = input( "DEBUG: Application Complete." )
