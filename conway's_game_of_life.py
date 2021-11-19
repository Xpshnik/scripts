"""The cellular automata simulation. Press Ctrl + C to stop."""

import copy, random, sys, time
from itertools import product

#Cell grid constants:
ALIVE = 'O'
DEAD = ' '
WIDTH = 80
HEIGHT = 20

next_cells = {}

for x in range(WIDTH):
    for y in range(HEIGHT):
        if random.randint(0, 1) == 1:
            next_cells[(x, y)] = ALIVE
        else:
            next_cells[(x, y)] = DEAD

while True:
    print('\n' * 20) #сlears the screen by printing some newlines

    cells = copy.deepcopy(next_cells)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(cells[x, y], end='')
        print()
    print('Press Ctrl+C to stop.')

    for x in range(WIDTH):
        for y in range(HEIGHT):
            left = (x - 1) % WIDTH
            right = (x + 1) % WIDTH
            above = (y - 1) % HEIGHT
            below = (y + 1) % HEIGHT

            neighbours_count = 0
            neighbours = list(product([left, x, right], [above, y, below]))
            del neighbours[4] #this excludes (x, y) coordinate

            for coord in neighbours:
                if cells[coord] == ALIVE:
                    neighbours_count += 1
            
            if cells[(x, y)] == ALIVE and (neighbours_count == 2 or neighbours_count == 3):
                next_cells[(x, y)] = ALIVE
            elif cells[(x, y)] == DEAD and neighbours_count == 3:
                next_cells[(x, y)] = ALIVE
            else:
                next_cells[(x, y)] = DEAD

    try:
        time.sleep(2)
    except KeyboardInterrupt:
        print("Conway's Game of Life")
        sys.exit()
