#! /usr/bin/env python2

from pyddl import *


def problem(verbose=True):
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
                ("travelled", "T1", "T2"),
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

    #Distances between starting positions and trash cans.
    distancemat = [
            [ 0, 10,  2,  4,  5,  7],
            [10,  0,  5,  6,  6,  3],
            [ 2,  5,  0,  4,  4,  5],
            [ 4,  6,  4,  0,  2,  3],
            [ 5,  6,  4,  2,  0,  2],
            [ 7,  3,  5,  3,  2,  0]
    ]

    def heuristic(state):
        cost = -max(max(distancemat))
        for p in state.predicates:
            if p[0] == "travelled":
                cost += distancemat[p[1]-1][p[2]-1]
        return cost


    return planner(problem, heuristic=heuristic, verbose=verbose)

if __name__ == "__main__":
    plan = problem()

    if plan is None:
        print("No plan!")
    else:
        for action in plan:
            print(action)

