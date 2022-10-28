from copy import deepcopy
import time
import pygame   
from OpenGL.GL import *
from collections import defaultdict, namedtuple

def pixel(x, y, width, height,color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(int(x),int(y),int(width),int(height))
    glClearColor(color[0],color[1],color[2],1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)


#VARIAVEIS
running = True
Dim = namedtuple("Dimension", ["width", "height"])
Grid = namedtuple("Grid", ["dim", "cells"])
Neighbours = namedtuple("Neighbours", ["alive", "dead"])
grid = Grid(Dim(50, 50), {(22, 8), (12, 7), (36, 7), (17, 9), (11, 8), (1, 9), (25, 4), (2, 8), (16, 7),
                                   (25, 10), (21, 6), (23, 9), (14, 6), (36, 6), (22, 7), (14, 12), (17, 8), (11, 10),
                                   (25, 9), (35, 7), (1, 8), (18, 9), (22, 6), (21, 8), (23, 5), (12, 11), (17, 10),
                                   (11, 9), (35, 6), (25, 5), (2, 9), (13, 6), (13, 12), (15, 9), (16, 11), (21, 7)})

#-------------------------------------------

def get_neighbours(grid: Grid, x: int, y: int) -> Neighbours:
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0),
               (1, 0), (-1, 1), (0, 1), (1, 1)]
    possible_neighbours = {(x + x_add, y + y_add) for x_add, y_add in offsets}
    alive = {(pos[0], pos[1])
             for pos in possible_neighbours if pos in grid.cells}
    return Neighbours(alive, possible_neighbours - alive)
    
def update_grid(grid: Grid) -> Grid:
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)

    for (x, y) in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)
        if len(alive_neighbours) not in [2, 3]:
            new_cells.remove((x, y))

        for pos in dead_neighbours:
            undead[pos] += 1

    for pos, _ in filter(lambda elem: elem[1] == 3, undead.items()):
        new_cells.add((pos[0], pos[1]))

    return Grid(grid.dim, new_cells)

#-------------------------------------------

def draw_grid(screen: pygame.Surface, grid: grid) -> None:
    cell_width = screen.get_width() / grid.dim.width
    cell_height = screen.get_height() / grid.dim.height
    border_size = 2

    for (x, y) in grid.cells:
        pixel(x* cell_width + border_size,y * cell_height + border_size,cell_width - border_size,cell_height - border_size,(255,0,0))
        # pygame.draw.rect(screen, (255, 0, 0), (x * cell_width + border_size, y * cell_height +
        #                                        border_size, cell_width - border_size, cell_height - border_size))

#-------------------------------------------

pygame.init()
screen = pygame.display.set_mode((600, 400), pygame.OPENGL | pygame.DOUBLEBUF)

while running:

    screen.fill((0, 0, 0))
    draw_grid(screen, grid)
    glClearColor(0,0,0,0)
    pygame.display.flip()
    time.sleep(0.1)
    glClear(GL_COLOR_BUFFER_BIT)
    grid = update_grid(grid)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


#-------------------------------------------

