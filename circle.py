#!/usr/bin/python
import pygame
import numpy as np

class Circle:
    def __init__(self, pos, radius):
        self.pos = np.array(pos, dtype='f')
        self.radius = np.float32(radius)
    def move(self, new_pos):
        self.pos = np.array(new_pos)
    def dmove(self, dpos):
        self.pos += np.array(dpos)
    def resize(self, new_radius):
        self.radius = new_radius
    def intersectCircle(self, other):
        return dist(self.pos, other.pos) <= self.radius + other.radius
    def toRect(self):
        diam = self.radius*2
        return pygame.Rect(self.pos - self.radius, (diam,diam))
    def __repr__(self):
        return "<circle((%.2f, %.2f), %.2f)>" % \
            (self.pos[0], self.pos[1], self.radius)

def dist(p1,p2):
    return np.linalg.norm(p1 - p2)
def test():
    A = Circle((0,0),5)
    B = Circle((11,0),6)
    print A, B, A.intersectCircle(B)
    B.move((12,0))
    print A, B, A.intersectCircle(B)
#test()
