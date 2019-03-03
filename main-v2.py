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

WORLD_SIZE = 64  # Is width & height.
CELL_SIZE = 8 # Is width & height.
CELL_APPEARANCE = 2  # Smaller means more cells.
VAL_RANGE = 300

# Cells are formatted: (hsv-outer, hsv-innner)
# -1 in the first slot means that there is no cell there: (-1, hue)
g_cell_array = []

def init():
    global g_cell_array

    random.seed()  # Init rng

    # Create 64*64 array of numbers. (an un-folded matrix)
    g_cell_array = [
        1 if random.randint(0, CELL_APPEARANCE) == 0 else 0
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

        if g_cell_array[i] == 2:
            pygame.draw.rect(DISPLAY_SURFACE, (255, 255, 255), r)  # Draws white Box
        elif g_cell_array[i] == 1:
            pygame.draw.rect(DISPLAY_SURFACE, (254/2, 254/2, 254/2), r)  # Draws white Box
        else:
            pygame.draw.rect(DISPLAY_SURFACE, (0, 0, 0), r)  # Draws Black Box

# This is the "do game math" function.
def update():
    global g_cell_array
    # Make a temp copy of the array to take values from.
    cell_array_cpy = g_cell_array.copy()

    # Iterate all cells and do operations on them.
    for i in range(0, len(g_cell_array)):
        side_sum = 0

        # down case.
        if i//WORLD_SIZE == WORLD_SIZE-1:
            side_sum += cell_array_cpy[i-(WORLD_SIZE**2-WORLD_SIZE)]
        else:
            side_sum += cell_array_cpy[i+WORLD_SIZE]

        # up case.
        if i//WORLD_SIZE == 0:
            side_sum += cell_array_cpy[i+(WORLD_SIZE**2-WORLD_SIZE)]
        else:
            side_sum += cell_array_cpy[i-WORLD_SIZE]

        if side_sum == 2:
            g_cell_array[i] = 2
        elif side_sum == 1:
            g_cell_array[i] = 0
        else:
            g_cell_array[i] = 1


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
