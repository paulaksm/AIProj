#! / track of the nodes in the rrt"
#usr/bin/env python2
# coding=utf8
'''
This file performes the pathfinding part of the application using rrt
This version does not use pytgame for drawing
'''

import numpy as np
import random
import taskalloc
import time
import argparse
from math import cos, sin, atan2, sqrt

SIZE = WIDTH, HEIGHT = 600, 600
ROBOT_WIDTH = 20
ROBOT_HEIGHT = 20
MAX_NODES = 100000
STEP_LENGTH = 10.0

walls = []
buff_walls = []

"keeps track of the nodes in the rrt"
class Node(object):
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent

"this is a replacement for pygame.rect() which was used in the"
"pygame version of this alogorithm"
class Rectangle(object):
    topleft = (0,0)
    bottomleft = (0,0)
    topright = (0,0)
    bottomright = (0,0)
    size = (0, 0)

    def __init__ (self, (x, y), (width, height)):
        "inits a rectangle"
        self.topleft = (x, y)
        self.bottomleft = (x, y + height)
        self.topright = (x + width, y)
        self.bottomright = (x + width, y + height)

    def collidepoint(self, (p1, p2)):
        "checks if a point is inside the rectangle"
        return p1 >= self.topleft[0] and p1 <= self.bottomright[0] and p2 >= self.topleft[1] and p2 <= self.bottomright[1]

def eucl_dist(p1,p2):
    "calculates the euclidian distance between two points"
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def eucl_distSq(p1,p2):
    "calculates the squared euclidian distance between two points"
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def init_map(filename):
    "inits the map"

    global walls
    global buff_walls

    trashcans = []
    robots = []

    f = open(filename, 'r')
    for line in f:
        "this parts reads input from a file"
        obj_list = line.split( )
        check_obj = obj_list[0]
        if (check_obj == 'r'):
            robots.append((int(obj_list[1]), int(obj_list[2])))
        elif (check_obj == 't'):
            trashcans.append((int(obj_list[1]), int(obj_list[2])))
        elif (obj_list[0] == 'w'):
            add_wall((int(obj_list[1]),int(obj_list[2])), (int(obj_list[3]),int(obj_list[4])))

    f.close()
    for r in robots:
        assert not(collides(r)), "robot at %s collides with a wall " % str(r)
    for t in trashcans:
        assert not(collides(t)), "trashcan at %s collides with a wall " % str(t)

    return robots, trashcans

def add_wall(corner, size):
    "Add a wall to the wall list"
    walls.append(Rectangle(corner, size))
    buff_corner = (corner[0] - ROBOT_WIDTH / 2, corner[1] - ROBOT_HEIGHT / 2)
    buff_size = (size[0] + ROBOT_WIDTH, size[1] + ROBOT_HEIGHT)
    buff_walls.append(Rectangle(buff_corner, buff_size))

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
    "calculates the next step in rrt"
    if eucl_distSq(p1,p2) < STEP_LENGTH ** 2:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + STEP_LENGTH*cos(theta), p1[1] + STEP_LENGTH*sin(theta)

"""
java.awt.geom.Line2D relativeCCW
"""
def relativeCCW(p1,p2,p):
    "cakcykates how a line will have to rotate to point to another point"
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
    "checks if some lines intersect or not"
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
    "this calculates the distance between two points in the rrt"
    "It first 'prunes' the rrt to make sure the path is as simple as possible"

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
        goal_dist += eucl_dist(curr_node.coord, curr_node.parent.coord)
        curr_node = curr_node.parent


    return goal_dist


def main():
    "init the argparser which is used to get the filename for the test case"
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file used to init the map")
    args = parser.parse_args()

    "used for timing the rrt"
    start_time = time.time()
    "inits robots, trashcans and walls from the input file"
    robots, trashcans = init_map(args.file)

    "some constants"
    N_ROBOTS = len(robots)
    N_TRASHCANS = len(trashcans)
    N_OBJECTS = N_TRASHCANS+N_ROBOTS
    "the distance matrix, will be used as input for the planner"
    dist_matrix = np.zeros([N_OBJECTS, N_OBJECTS])
    "some lists for trashcans and the nodes"
    trashcan_status = []
    node_lists = [[] for i in range(N_OBJECTS)]


    "Initialize robots into nodes"
    for i in range(N_ROBOTS):
        node_lists[i].append(Node(robots[i], None))

    "Initialize trashcans into nodes"
    for i in range(N_TRASHCANS):
        trashcan_status.append((trashcans[i], False, Node(None, None)))
        node_lists[i+N_ROBOTS].append(Node(trashcans[i], None))

    "some variables used to running the program"
    curr_state = 'init'
    running = True
    goal = False

    goal_node = Node(None, None)
    count = 0

    "Distance between robots"
    if i in range(N_ROBOTS):
        if j in range(N_ROBOTS):
            dist_matrix[i][j] = 10**14

    goal_dist = []
    nodes = []


    while running:

        if curr_state == 'build':

            "Build tree from each startnode and goal"
            for i in range(N_OBJECTS):

                count += 1
                if count < MAX_NODES:
                    foundNext = False
                    while foundNext == False:
                        rand = new_coord()
                        parent = node_lists[i][0]

                        "Find closest node in current tree"
                        for p in node_lists[i]:
                            if eucl_distSq(p.coord, rand) <= eucl_distSq(parent.coord, rand):
                                newPoint = new_step(p.coord, rand)
                                if collides(newPoint) == False and obstaclefree(p.coord, newPoint):
                                    parent = p
                                    foundNext = True

                    "Connect new point to closest node"
                    newnode = new_step(parent.coord, rand)
                    node_lists[i].append(Node(newnode,parent))

                    "Check if new point collides with any other object"
                    for obj in range(N_OBJECTS):
                        if (obj == i):
                            continue
                        if point_coll(node_lists[obj][0].coord, newnode, 10) and dist_matrix[i, obj] == 0:
                            dist_matrix[i, obj] = calc_dist(node_lists[i][-1])
                            dist_matrix[obj, i] = dist_matrix[i, obj]
                            "uncomment these to see the distance matrix build itself"
                            #print(dist_matrix.astype(int))


        "would draw trashcans and robots if this was the pygame version"
        if curr_state == 'init':
            curr_state = 'build'

        "Check if all paths found"
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

    if(goal):
        "the distance matrix is complete, send input to planner"
        print("Goal reached in %.2f seconds" % (time.time() - start_time))
        print(dist_matrix.astype(int))
        taskalloc.get_plan(dist_matrix.astype(int), N_ROBOTS, True)

if __name__ == '__main__':
    main()
