#! /usr/bin/env python2

from pyddl import *
from planner import *
import re

def problem(distancemat, verbose=True, maxplans=20):
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
            )
        ),
    ))
    problem = Problem(
        domain,
        {
            # List of all agents
            "agent" : ("a", "b"),
            #list of trash cans. Note: Starting positions are treated as trash cans.
            "trash_can" : (1, 2, 3, 4, 5, 6),
        },

        init=(
            ("at", "a", 1),
            ("at", "b", 2),
        ),

        goal=(
                # 1 and 2 are starting positions, and as such ignored here.
                ("checked", 3),
                ("checked", 4),
                ("checked", 5),
                ("checked", 6),
        )
    )

    # Heuristics based on the agent that has travelled the farthest
    def heuristic(state):
        cost = -max(max(distancemat))
        agent2cost = {}
        for p in state.predicates:
            if p[0] == "travelled":
                if not(p[1] in agent2cost):
                    agent2cost[p[1]] = cost
                agent2cost[p[1]] += distancemat[p[2]-1][p[3]-1]
        # add cost to values list in case agent2cost is empty
        return max(agent2cost.values() + [cost])


    return planner(problem, heuristic=heuristic, verbose=verbose, maxplans=maxplans)

if __name__ == "__main__":
    #Distances between starting positions and trash cans.
    distancemat = [
            [ 0, 10,  2,  4,  5,  7],
            [10,  0,  5,  6,  6,  3],
            [ 2,  5,  0,  4,  4,  5],
            [ 4,  6,  4,  0,  2,  3],
            [ 5,  6,  4,  2,  0,  2],
            [ 7,  3,  5,  3,  2,  0]]

    plans = problem(distancemat, False, maxplans=20)

    times = []
    for plan in plans:
        if plan is None:
            print("No plan!")
        else:
            #   (agent, from, to)
            #   ('a', 1, 3)
            # turn _grounded somthing into a tuple 
            tupledPlan = [tuple(re.sub(r'[(),]'," ", str(act)).split()) for act in plan]
            
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
            times.append((time,totalDistance,))

    argmin = times.index(min(times))

    print("greedy:\ttime = %d, distance = %d" % times[0])
    for action in plans[0]:
        print(action)
    print("best:\ttime = %d, distance = %d" % times[argmin])
    for action in plans[argmin]:
        print(action)


