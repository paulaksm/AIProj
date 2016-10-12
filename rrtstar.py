#! /usr/bin/env python2
# coding=utf8
'''
Working distance matrix version
'''

"constants used for drawing"

from pygame.locals import *
import pygame
import numpy as np
import random
import taskalloc
import time
from math import cos, sin, atan2, sqrt

SIZE = WIDTH, HEIGHT = 600, 600
N_TRASHCANS = 7
N_ROBOTS = 3
N_OBJECTS = N_TRASHCANS+N_ROBOTS
ROBOT_WIDTH = 20
ROBOT_HEIGHT = 20
MAX_NODES = 100000
STEP_LENGTH = 10.0
RADIUS = 3

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

walls = []
buff_walls = []
node_lists = [[] for i in range(N_OBJECTS)]

class Node(object):
    cost = 0
    parent = None
    def __init__(self, coord):
        self.coord = coord

def eucl_dist(p1,p2):
    "calculates the euclidian distance between two points"
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def eucl_distSq(p1,p2):
    "calculates the squared euclidian distance between two points"
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def init_map():
    "inits the map"
    global walls
    global buff_walls

    add_wall((50,80),(120,320))
    add_wall((0,380),(50,20))
    add_wall((400,200),(400,200))
    add_wall((200,0),(100,175))

    for i in walls:
        pygame.draw.rect(screen, (100, 100, 100), i)

def add_wall(corner, size):
    walls.append(pygame.Rect(corner, size))
    buff_corner = (corner[0] - ROBOT_WIDTH / 2, corner[1] - ROBOT_HEIGHT / 2)
    buff_size = (size[0] + ROBOT_WIDTH, size[1] + ROBOT_HEIGHT)
    buff_walls.append(pygame.Rect(buff_corner, buff_size))

def collides(p):
    "checks if a rectangle collides with the walls"
    for i in buff_walls:
        if i.collidepoint(p):
            return True
    return False

def new_coord():
    "return a new coordinate"
    while True:
        temp = np.random.random()*WIDTH, np.random.random()*HEIGHT
        if not(collides(temp)):
            return temp

def point_coll(p1, p2, radius):
    "checks if a point is within a certian radius of another point"
    if eucl_distSq(p1,p2) < radius ** 2:
        return True
    return False


def new_step(p1, p2):
    "calculates the next step"
    if eucl_distSq(p1,p2) < STEP_LENGTH ** 2:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + STEP_LENGTH*cos(theta), p1[1] + STEP_LENGTH*sin(theta)

"""
java.awt.geom.Line2D relativeCCW
"""
def relativeCCW(p1,p2,p):
    a = p2[0] - p1[0], p2[1] - p1[1]
    b = p[0] - p1[0], p[1] - p1[1]
    ccw = b[0] * a[1] - b[1] * a[0]
    if ccw == 0.0:
        ccw = b[0] * a[0] + b[1] * a[1]
        if ccw > 0.0:
            b = b[0] - a[0], b[1] - a[1]
            ccw = b[0] * a[0] + b[1] * a[1]
            if ccw < 0.0:
                ccw = 0.0
    if ccw < 0:
        return -1
    if ccw > 0:
        return 1
    return 0
"""
java.awt.geom.Line2D linesIntersect
"""
def linesIntersect(p1, p2, p3, p4):
    return ((relativeCCW(p1,p2,p3) * relativeCCW(p1,p2,p4) <= 0) and
        (relativeCCW(p3,p4,p1) * relativeCCW(p3,p4,p2) <= 0))

def obstaclefree(p1, p2):
    "checks if there are no walls between two points"
    t = np.arange(0, 1, 0.05)
    for wall in buff_walls:
        corners = [wall.topleft, wall.bottomleft, wall.bottomright,
            wall.topright, wall.topleft]
        for it in range(4):
            if linesIntersect(p1, p2, corners[it], corners[it+1]):
                return False
    return True

def calc_dist(curr_node):

    temp = curr_node
    goal_dist = 0

    # Try to shorten and smoothen out path
    while curr_node.parent != None:
        if (curr_node.parent.parent != None and obstaclefree(curr_node.coord, curr_node.parent.parent.coord)):
            curr_node.parent = curr_node.parent.parent
        else:
            curr_node = curr_node.parent

    curr_node = temp

    # Calculate distance (and draw path)
    while curr_node.parent != None:
        pygame.draw.line(screen, (150, 100, 50), curr_node.coord, curr_node.parent.coord, 1)
        goal_dist += eucl_dist(curr_node.coord, curr_node.parent.coord)
        curr_node = curr_node.parent


    return goal_dist

def rewire(newnode, i):
    for k in range(len(node_lists[i])):
        temp = node_lists[i][k]
        dist = eucl_dist(temp.coord, newnode.coord)
        if temp != newnode.parent and dist < RADIUS and newnode.cost + dist < temp.cost:
            temp.parent = newnode
            temp.cost = newnode.cost + dist
            node_lists[i][k] = temp

def chooseParent(parent, newnode, i):
    for k in node_lists[i]:
        dist = eucl_dist(k.coord, newnode.coord)
        if dist < RADIUS and k.cost+dist < parent.cost+eucl_dist(parent.coord, newnode.coord):
            parent = k
        newnode.cost = parent.cost+eucl_dist(parent.coord, newnode.coord)
        newnode.parent = parent
        return newnode, parent


def main():
    pygame.init()

    start_time = time.time()
    dist_matrix = np.zeros([N_OBJECTS, N_OBJECTS])
    trashcan_status = []
    init_map()


    "Initialize robots randomly"
    robots = np.random.randint(50, 600-50, (N_ROBOTS, 2))
    for i in range(N_ROBOTS):
        while collides((robots[i][0], robots[i][1])):
            robots[i] = np.random.randint(50, 600-50, 2)
        node_lists[i].append(Node(robots[i]))

    "Initialize trashcans randomly"
    trashcans = np.random.randint(50, 600-50, (N_TRASHCANS, 2))
    for i in range(N_TRASHCANS):
        while collides((trashcans[i][0], trashcans[i][1])):
            trashcans[i] = np.random.randint(50, 600-50,2)
        trashcan_status.append((trashcans[i], False, Node(None)))
        node_lists[i+N_ROBOTS].append(Node(trashcans[i]))

    curr_state = 'init'
    running = True
    goal = False

    goal_node = Node(None)
    count = 0


    goal_dist = []
    nodes = []


    while running:

        if curr_state == 'build':

            # Build tree from each startnode and goal
            for i in range(N_OBJECTS):

                count += 1
                if count < MAX_NODES:
                    foundNext = False
                    parent = node_lists[i][0]
                    while foundNext == False:
                        rand = new_coord()

                        # Find closest node in current tree 
                        for p in node_lists[i]:
                            if eucl_distSq(p.coord, rand) <= eucl_distSq(parent.coord, rand):
                                newPoint = new_step(p.coord, rand)
                                if collides(newPoint) == False and obstaclefree(p.coord, newPoint):
                                    parent = p
                                    foundNext = True

                    # Connect new point to closest node 
                    newnode = Node(new_step(parent.coord, rand))
                    newnode, parent = chooseParent(parent, newnode, i)
                    node_lists[i].append(newnode)
                    pygame.draw.line(screen, (255,255,255), newnode.coord, parent.coord)

                    rewire(newnode, i)

                    # Check if new point collides with any other object 
                    for obj in range(N_OBJECTS):
                        if (obj == i):
                            continue
                        if point_coll(node_lists[obj][0].coord, newnode.coord, 10) and dist_matrix[i, obj] == 0:
                            dist_matrix[i, obj] = calc_dist(node_lists[i][-1])
                            dist_matrix[obj, i] = dist_matrix[i, obj]
                            print(dist_matrix)
                            print(obj)


        # Draw trashcans and robots
        if curr_state == 'init': 
            for idx, i in enumerate(robots):
                pygame.draw.ellipse(screen, (150, 100, 150), [i[0] - ROBOT_WIDTH/2, i[1] - ROBOT_HEIGHT/2, ROBOT_WIDTH, ROBOT_HEIGHT])

            for idx, i in enumerate(trashcans):
                pygame.draw.circle(screen, (0, 255, 255) , [i[0],i[1]], 10)
            curr_state = 'build'

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Check if all paths found
        NODES_DONE = 0
        for i in range(N_OBJECTS):
            for j in range(N_OBJECTS):
                if (i == j):
                    continue
                if dist_matrix[i, j] != 0:
                    NODES_DONE += 1
        if NODES_DONE == N_OBJECTS * N_OBJECTS - N_OBJECTS:
            goal = True
            running = False
        pygame.display.update()

    if(goal):
        print("Goal reached in %.2f seconds, some info" % (time.time() - start_time))
        print(dist_matrix)
        taskalloc.get_plan(dist_matrix.astype(int)/10, N_ROBOTS, True)
        pygame.time.wait(3000)
    #pygame.quit()

if __name__ == '__main__':
    main()
