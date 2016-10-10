#!/usr/bin/python
import pygame
import numpy as np
SIZE = WIDTH, HEIGHT = 400, 400
GRID = 10


"""
Get all squares it collides with.
p1: minX, minY
p2: maxX, maxY
"""
def rectGridIntersect(minP, maxP):
    minP = minP[0] / GRID, minP[1] / GRID
    maxP = (maxP[0]-1) / GRID, (maxP[1]-1) / GRID
    coords = []
    for i in range(minP[0], maxP[0]+1):
        for j in range(minP[1], maxP[1]+1):
            corners = [(i, j), (i + 1, j), (i, j + 1), (i + 1,j + 1)]
            coords.append(corners)
    return coords

def distSq(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2
"""
Remove rectangles that does not intersect with the circle
"""
def filterRects(pos, radius, coords):
    is_inside = []
    for ind, sqCoords in enumerate(coords):
        for sqPos in sqCoords:
            if distSq(np.multiply(sqPos, GRID), pos) < radius ** 2:
                is_inside.append(coords[ind][0])
                break
    return is_inside
"""
Find the grids the circle intersect with
"""
def circleGridIntersect(pos, radius):
    gridSquares = rectGridIntersect((pos[0] - radius,pos[1] - radius), (pos[0] + radius,pos[1] + radius))
    return filterRects(pos, radius, gridSquares)

class CollisionGrid:
    def __indx(self,i,j):
        return self.size[1] * i + j
    def __init__(self, SIZE, grid_size):
        self.size = SIZE[0] / grid_size, SIZE[1] / grid_size
        self.space = [False for i in range(self.size[0] * self.size[1])]
    """
    Set all spaces to unoccupied (False)
    """
    def reset(self):
        self.space = [False for i in range(self.size[0] * self.size[1])]
    """
    Set all spaces in grids to True
    """
    def occupy(self, grids):
        for i, j in grids:
            self.space[self.__indx(i,j)] = True
    """
    Check if any of grids are already occupied.
    returns True if a collision is found
    """
    def collides(self, grids):
        for i, j in grids:
            if self.space[self.__indx(i,j)]:
                return True
        return False
    """
    Get spaces that are occupied
    """
    def getOccupied(self):
        occ = []
        for i in range(self.size[0]):
            for j in range(self.size[0]):
                if self.space[self.__indx(i,j)]:
                    occ.append((i,j))
        return occ
def test():
    "Create an ellipse"
    ellipse = pygame.Rect((301,321), (40,40))
    "Find the grids it occupies"
    occupiedGrids = circleGridIntersect(ellipse.center, 20)
    "Create a map to detect collision"
    collisionGrid = CollisionGrid(SIZE, GRID)
    "Check if the circle collides with anything in the grid"
    print collisionGrid.collides(occupiedGrids)
    assert not(collisionGrid.getOccupied())
    "Occupy/book the grids the circle occupies"
    collisionGrid.occupy(occupiedGrids)
    "Check if the circle collides with anything in the grid"
    print collisionGrid.collides(occupiedGrids)
    assert collisionGrid.getOccupied()

test()
