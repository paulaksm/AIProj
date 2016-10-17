#! /usr/bin/env python2
# coding=utf8
from pyddl import Action, Domain, Problem, planner, neg
# from planner import *
import re
import numpy as np


def problem(distancemat, agentcount, verbose=True):
    agents = [i for i in range(agentcount)]
    trashcount = len(distancemat) - agentcount
    trash_cans = [i + agentcount for i in range(trashcount)]
    agentDict = dict([(i,0) for i in agents])
    domain = Domain((
        Action(
            "Check",
            # Send agent A1 from T1 to pick up trash at T2
            parameters=(
                ("agent", "A1"),
                ("trash_can", "T1"),
                ("trash_can", "T2"),
            ),
            preconditions=(
                ("at", "A1", "T1"),
                ("unchecked", "T2"),
            ),
            effects=(
                # A1 is no longer at T1
                neg(("at", "A1", "T1")),
                # A1 is now at T2
                ("at", "A1", "T2"),
                # T2 is checked.
                ("checked", "T2"),
                neg(("unchecked", "T2")),
            )
        ),
    ))
    problem = Problem(
        domain,
        {
            # List of all agents
            "agent":  agents,
            # list of trash cans. Note: Starting positions are
            # treated as trash cans.
            "trash_can":  [i for i in range(len(distancemat))],
        },
        init=[("at", i, i) for i in agents] + \
                [("unchecked", i) for i in trash_cans],
        goal=[("checked", i) for i in trash_cans]
    )
    # Heuristics based on the agent that has travelled the farthest
    def heuristic(state):
        # copy prepared table
        agent2cost = agentDict.copy()
        # calculate cost
        for a in [action.sig for action in state.plan()]:
            agent2cost[a[1]] += distancemat[a[2]][a[3]]
        cost = max(agent2cost.values())
        #heur = ?
        return cost

    return planner(problem,
                   heuristic=heuristic,
                   verbose=verbose)

def get_plan(distancemat, agentcount , verbose=False, pop=False):
    """
        Returns a dictionary of with allocated trash cans for every agent.
        <pop> sets ordering of targets. True -> reversed order, for pop()-support.
    """

    assert(agentcount > 0)

    plan = problem(distancemat, agentcount, verbose)
    if plan is None:
        return dict()
    #   (agent, from, to)
    #   ('a', 1, 3)
    # turn _grounded somthing into a tuple
    tupledPlan = [act.sig for act in plan]
    # list of all agents
    agents = [i for i in range(agentcount)]
    # initialize
    allocation_dict = dict()
    for agent in agents:
        allocation_dict[agent] = list()
    # populate

    for action in tupledPlan:
        if pop:
            allocation_dict[action[1]].insert(0, action[3])
        else:
            allocation_dict[action[1]].append(action[3])

    agent2time = dict([(i, 0) for i in agents])
    #  sum costs of this path (from the matrix)
    for act in tupledPlan:
        agent2time[act[1]] += distancemat[act[2]][act[3]]

    time = max(agent2time.values())
    totalDistance = sum(agent2time.values())
    
    if verbose:
        print("time: %d,\tdistance: %d" % (time, totalDistance))
        for action in plan:
            print(action)

    allocation_dict["time"] = time
    allocation_dict["distance"] = totalDistance

    return allocation_dict


if __name__ == "__main__":
# Distances between starting positions and trash cans.
    distancemat =  [
        [0, 10,  2,  4,  5,  7],
        [10, 0,  5,  6,  6,  3],
        [2,  5,  0,  4,  4,  5],
        [4,  6,  4,  0,  2,  3],
        [5,  6,  4,  2,  0,  2],
        [7,  3,  5,  3,  2,  0]]

    plan = get_plan(distancemat, 2, True)
    print("-------")
    print(plan)
