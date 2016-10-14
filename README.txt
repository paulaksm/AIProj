
We coded this project in Python 2. 
For this project we coded the RRT algorithm ourselves based off the sources we found. 
For the pddl we used a library called PyDDL. 
A heuristic used in the planner was also coded by us however. 

File descriptions:

rrt.py
Performs one round of rrt on the test case provided. 
It also draws the environment using the pygame library. 

rrt_nopygame.py
same algorithm as the one above, however pygame functionallity has been removed. 

rrtconnect.py
another version of rrt. 
NOTE: we did not manage to finish this one, as it’s still kinda bugged but we would like to demonstrate the limited functionality we have at the presentation to show how you could maybe make this planning faster. 

rrtstar.py
performs the rrt star algorihm. 
Draws it with pygame. You can run this file as ‘python2 rrtstar.py RANDOM’ to generate random trashcans and robots in the ‘default’ environment. 

rrtstar_nopygame.py
same as the one above but without pygame functions. 

taskalloc.py
the functions in this file are used in the rrt algorithm files. 
The distance matrix found by the rrt and how many of the spots are robots are sent here and the pddl planning is done. 
You do not need to run this file yourself.

default.map
our ‘default’ test case. 
Can be used as input for the rrt files. 

simple.map
a simple test case.

tk14.map
a somewhat faithfull recreation of some floor on Teknikringen 14.

We have also included a folder with PyDDL which was used in our project. 

How to run:
First of all: you need to run the project with python2!
We used a few libraries in this project. Two of these that you need are numpy and pyddl. 
If you want to see the rrt process drawn you also need the pygame package for python. 
These packages need to be installed for python2. 
The pyddl package has been included and can be installed by going to the PyDDL/pyddl folder and running 

>sudo python2 setup.py install

When this is done you can run the files using the following commands (for these examples we use the tk14.map test case):
>python2 rrt.py tk14.map

>python2 rrt_nopygame.py tk14.map

>python2 rrtstar.py tk14.map

or
>python2 rrtstar_nppygame.py tk14.map

Creating test cases:
to create a testcase just make a file (we used the .map filetype but you can use whatever)
to add a robot you need to add a line that looks like this:
r <x-coord> <y-coord>

to add a trash can you need to add a line like this:
t <x-coord> <y-coord>

to add a wall you add a line that looks like this:
w <x-coord> <y-coord> <wall width> <wall height>

make sure there are no empty lines!
