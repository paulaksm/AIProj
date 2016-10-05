'''
Simple concept environment implemented in pygame.
Testing if it would be suitable as some kind of
visualization for the project
'''


from pygame.locals import *
import pygame
import numpy as np
import random
from math import cos, sin, atan2, sqrt

SIZE = WIDTH, HEIGHT = 600, 600
N_TRASHCANS = 1
N_ROBOTS = 1
MAX_NODES = 10000

screen = pygame.display.set_mode(SIZE);
clock = pygame.time.Clock()

walls = []

class Node(object):
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent

def eucl_dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def init_map():
    global walls

    walls.append(pygame.Rect((50,20),(120,240)))
    walls.append(pygame.Rect((400,200),(400,200)))
    
    for i in walls:
        pygame.draw.rect(screen, (100,100,100), i)

def collides(p):
    for i in walls:
        if i.collidepoint(p):
            return True
    return False

def new_coord():
    while True:
        temp = np.random.random()*WIDTH, np.random.random()*HEIGHT
        if not(collides(temp)):
            return temp

def goal_coll(p1, p2, radius):
    if eucl_dist(p1,p2) < radius:
        return True
    return False


def new_step(p1, p2):
    if eucl_dist(p1,p2) < 5.0:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + 5.0*cos(theta), p1[1] + 5.0*sin(theta)

def main():
    pygame.init()
    

    # Initialize trashcans randomly
    trashcans = np.random.randint(50, 600-50, (N_TRASHCANS, 2))
    
    
    # Robot node (root of tree)
    init_node = Node([300, 300], None)
    nodes = []
    nodes.append(init_node)


    init_map()
    curr_state = 'build'


    running = True
    goal = False

    goal_node = Node(None, None)
    count = 0
    
    goal_dist = 0

    robot = [300, 300]
    objRobot = pygame.Rect([robot[0], robot[1], 10, 10])


    while running:

        if curr_state == 'build':
            count += 1 
            if count < MAX_NODES:
                foundNext = False
                while foundNext == False:
                    rand = new_coord() 
                    parent = nodes[0]

                    for p in nodes:
                        if eucl_dist(p.coord, rand) <= eucl_dist(parent.coord, rand):
                            newPoint = new_step(p.coord, rand)
                            if collides(newPoint) == False:
                                parent = p
                                foundNext = True
                            
                newnode = new_step(parent.coord, rand)
                nodes.append(Node(newnode,parent))
                pygame.draw.line(screen, (255,255,255), parent.coord, newnode)
                
                if goal_coll(trashcans[0], newnode, 10):
                    goal = True
                    goal_node = nodes[-1]
                    curr_state = 'goal_found'
        
        if curr_state == 'goal_found':

            curr_node = goal_node.parent
            while curr_node.parent != None:
                pygame.draw.line(screen, (150,50,0), curr_node.coord, curr_node.parent.coord, 5)
                goal_dist += eucl_dist(curr_node.coord, curr_node.parent.coord)
                curr_node = curr_node.parent
              
                #trashcans[0].coord[0] += 
            
            running = False

        for idx, i in enumerate(trashcans):
            pygame.draw.circle(screen, (0, 255, 255) , [i[0],i[1]], 10) 
            if (pygame.Rect(i[0],i[1],10,10).colliderect(objRobot)):
                trashcans = np.delete(trashcans, np.s_[idx:idx+1], axis=0)
                print("Checked trashcan", idx)


        pygame.draw.rect(screen, (255, 255, 255), objRobot)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False 


        pygame.display.update()


    if(goal):
        print("Goal reached in blabla sec, some info")
        print(goal_dist)
        pygame.time.wait(3000)
    #pygame.quit()

if __name__ == '__main__':
    main()
