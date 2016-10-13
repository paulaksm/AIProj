#! /usr/bin/env python2
# coding=utf8
from pyddl import Action, Domain, Problem, planner, neg
# from planner import *
import re
import numpy as np


def problem(distancemat, agentcount, verbose=True):
    trashcount = len(distancemat) - agentcount
    domain = Domain((
        Action(
            "pick-up",
            # Send agent A1 from T1 to pick up trash at T2
            parameters=(
                ("agent", "A1"),
                ("trash_can", "T1"),
                ("trash_can", "T2"),
            ),
            preconditions=(
                ("at", "A1", "T1"),
                ("unchecked", "T2"), # Klarar inte neg(("checked","T2"))
            ),
            effects=(
                # This predicate is used to find the distance travelled
                # by the agent. (heuristic function)
                ("travelled", "A1", "T1", "T2"),
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
            "agent":  [i for i in range(agentcount)],
            # list of trash cans. Note: Starting positions are
            # treated as trash cans.
            "trash_can":  [i for i in range(len(distancemat))],
        },
        init=[("at", i, i) for i in range(agentcount)] +\
            [("unchecked", i + agentcount) for i in range(trashcount)],
        goal=[("checked", i + agentcount) for i in range(trashcount)]
    )
    # Heuristics based on the agent that has travelled the farthest
    def heuristic(state):
        #print distancemat
        agent2cost = {}
        for p in state.predicates:
            if p[0] == "travelled":
                if not(p[1] in agent2cost):
                    agent2cost[p[1]] = 0
                agent2cost[p[1]] += distancemat[p[2]][p[3]]
                #agent2cost[p[1]] += distancemat[p[2]-1][p[3]-1]
        # add cost to values list in case agent2cost is empty
        return max(agent2cost.values() + [0])

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
    tupledPlan = [tuple(re.sub(r'[(),]', " ", str(act)).split())
                  for act in plan]

    # initialize
    allocation_dict = dict()
    for agent in range(agentcount):
        allocation_dict[agent] = []
    # populate
    for action in tupledPlan:
        if pop:
            allocation_dict[int(action[1])].insert(0, int(action[3]))
        else:
            allocation_dict[int(action[1])].append(int(action[3]))


    agent2time = dict()
    #  sum costs of this path (from the matrix)
    for act in tupledPlan:
        # if not(act[0] == 'pick-up'): continue
        agent, l1, l2 = act[1], int(act[2])-1, int(act[3])-1
        if not(agent in agent2time):
            agent2time[agent] = 0
        agent2time[agent] += distancemat[l1][l2]

    time = max(agent2time.values())
    totalDistance = sum(agent2time.values())
    # We can give different weight to time and distance
    # Currently, time is top priority
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
