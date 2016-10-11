#! /usr/bin/env python2
# coding=utf8
'''
Simple concept environment implemented in pygame.
Testing if it would be suitable as some kind of
visualization for the project
'''

"constants used for drawing"

from pygame.locals import *
import pygame
import numpy as np
import random
from math import cos, sin, atan2, sqrt

SIZE = WIDTH, HEIGHT = 600, 600
N_TRASHCANS = 5
N_ROBOTS = 3
ROBOT_WIDTH = 20
ROBOT_HEIGHT = 20
MAX_NODES = 10000
STEP_LENGTH = 10.0

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

walls = []

class Node(object):
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent

def eucl_dist(p1,p2):
    "calculates the culidian distance between two points"
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def init_map():
    "inits the map"
    global walls

    walls.append(pygame.Rect((50,80),(120,320)))
    walls.append(pygame.Rect((0,380),(50,20)))
    walls.append(pygame.Rect((400,200),(400,200)))
    walls.append(pygame.Rect((200,0),(100,175)))

    for i in walls:
        pygame.draw.rect(screen, (100, 100, 100), i)

def collides(p):
    "checks if a rectangle collides with the walls"
    for i in walls:
        if i.colliderect(pygame.Rect([p[0] - ROBOT_WIDTH/2, p[1] - ROBOT_HEIGHT/2, ROBOT_WIDTH, ROBOT_HEIGHT])):
            return True
    return False

def new_coord():
    "return a new coordinate"
    while True:
        temp = np.random.random()*WIDTH, np.random.random()*HEIGHT
        if not(collides(temp)):
            return temp

def goal_coll(p1, p2, radius):
    "checks if a point is within a certian radius of another point"
    if eucl_dist(p1,p2) < radius:
        return True
    return False


def new_step(p1, p2):
    "calculates the next step"
    if eucl_dist(p1,p2) < STEP_LENGTH:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + STEP_LENGTH*cos(theta), p1[1] + STEP_LENGTH*sin(theta)

def obstaclefree(p1, p2):
    "checks if there are no walls between two points"
    t = np.arange(0, 1, 0.05)
    for ti in t:
        x = p1[0] + (p2[0] - p1[0]) * ti;
        y = p1[1] + (p2[1] - p1[1]) * ti;
        if collides((x,y)):
            return False

    return True

def main():
    pygame.init()

    trashcan_status = []

    init_map()
    curr_state = 'build'

    "Initialize trashcans randomly"
    trashcans = np.random.randint(50, 600-50, (N_TRASHCANS, 2))
    for i in range(N_TRASHCANS):
        while collides((trashcans[i][0], trashcans[i][1])):
            trashcans[i] = np.random.randint(50, 600-50,2)
        trashcan_status.append((trashcans[i], False, Node(None, None)))


    "for debug, static trashcan behind wall"
    #trashcans[0] = (500, 180)
    #trashcans[0] = (25, 350)
    #while True:
    #    trashcans[0] = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    #    if not collides(trashcans[0]):
    #        break

    running = True
    goal = False

    goal_node = Node(None, None)
    count = 0

    goal_dist = []
    nodes = []

    "Initialize robots"
    robots = np.random.randint(50, 600-50, (N_ROBOTS, 2))
    for i in range(N_ROBOTS):
        while collides((robots[i][0], robots[i][1])):
            robots[i] = np.random.randint(50, 600-50, 2)

    curr_robot = 0

    while running:

        if curr_state == 'build':
            #print(robots[curr_robot])
            init_node = Node(robots[curr_robot], None)
            nodes.append(init_node)
            count += 1
            if count < MAX_NODES:
                foundNext = False
                while foundNext == False:
                    rand = new_coord()
                    parent = nodes[0]

                    for p in nodes:
                        if eucl_dist(p.coord, rand) <= eucl_dist(parent.coord, rand):
                            newPoint = new_step(p.coord, rand)
                            if collides(newPoint) == False and obstaclefree(p.coord, newPoint):
                                parent = p
                                foundNext = True

                newnode = new_step(parent.coord, rand)
                nodes.append(Node(newnode,parent))
                pygame.draw.line(screen, (255,255,255), parent.coord, newnode)
                trashcans_found = 0
                for tc in range(N_TRASHCANS):
                    if goal_coll(trashcan_status[tc][0], newnode, 10) and not trashcan_status[tc][1]:
                        trashcan_status[tc] = (trashcans[tc], True, nodes[-1])
                    if trashcan_status[tc][1]:
                        trashcans_found += 1
                if trashcans_found == N_TRASHCANS:
                    goal = True
                    curr_state = 'goal_found'

        if curr_state == 'goal_found':
            for numerator in range(N_TRASHCANS):
                goal_dist.append(0)
                curr_node = trashcan_status[numerator][2]
                while curr_node.parent != None:
                    if curr_node.parent.parent != None and obstaclefree(curr_node.coord, curr_node.parent.parent.coord):
                        curr_node.parent = curr_node.parent.parent
                    else:
                        curr_node = curr_node.parent

                curr_node = trashcan_status[numerator][2]
                while curr_node.parent != None:
                    pygame.draw.line(screen, (150, 50, 0), curr_node.coord, curr_node.parent.coord, 5)
                    goal_dist[numerator] += eucl_dist(curr_node.coord, curr_node.parent.coord)
                    curr_node = curr_node.parent
            trashcans_found = 0;
            for i in range(N_TRASHCANS):
                trashcan_status[i] = (trashcans[i], False, nodes[-1])
            print(curr_robot)
            if curr_robot != N_ROBOTS-1:
                curr_state = 'build'
            else:
                goal = True
                running = False
            nodes = []
            curr_robot += 1
                #trashcans[0].coord[0] +=

            #running = False

        for idx, i in enumerate(robots):
            pygame.draw.rect(screen, (150, 100, 150), [i[0] - ROBOT_WIDTH/2, i[1] - ROBOT_HEIGHT/2, ROBOT_WIDTH, ROBOT_HEIGHT])

        for idx, i in enumerate(trashcans):
            pygame.draw.circle(screen, (0, 255, 255) , [i[0],i[1]], 10)
        #    if (pygame.Rect(i[0],i[1],10,10).colliderect(objRobot)):
        #        trashcans = np.delete(trashcans, np.s_[idx:idx+1], axis=0)
        #        print("Checked trashcan", idx)

        #pygame.draw.rect(screen, (255, 0, 255), objRobot)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False


        pygame.display.update()

    if(goal):
        print("Goal reached in blabla sec, some info")
        for i in range(N_TRASHCANS):
            print(goal_dist[i])
        pygame.time.wait(3000)
    #pygame.quit()

if __name__ == '__main__':
    main()
