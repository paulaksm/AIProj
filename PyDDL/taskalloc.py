#! /usr/bin/env python2

from pyddl import *


agent1 = {
        "start": 13,
        "paths": [([ 1, 3],    [13,  9,  5, 1, 2, 3]),
                  ([11, 3],    [13, 14, 11, 7, 3])   ]
         }
agent2 = {
        "start": 9,
        "paths": [ ([15, 12],  [9, 13, 14, 15, 16, 12]),
                   ([12, 15],  [9, 10, 11, 12, 16, 15]) ]
         }



def problem(agents, trashcans, verbose=True):
    #find longest path, and set timeline accordingly
    max_path_len = 0
    for agent in agents:
        paths = agent["paths"]
        for path in paths:
            if len(path[1]) > max_path_len:
                max_path_len = len(path[1])

    domain = Domain((

    ))
    problem = Problem(
        domain,
        {
            "agent" : [i for i in range(len(agents))],
            "trashcan" : [i for i in range(len(trashcans))]
        },
        init=(
        ),
        goal=(
        )
    )
    #domain = Domain((
    #))




if __name__ == "__main__":
    problem([agent1, agent2])
