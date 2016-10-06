#! /usr/bin/env python2

from pyddl import *


def problem(verbose=True):
    domain = Domain((
        Action( #allocate a time/space frame to an agent.
            "pick-up",
            parameters=(
                ("agent", "A1"),
                ("trashcan", "T1"),
                ("trashcan", "T2"),
            ),
            preconditions=(
                ("at", "A1", "T1"),
                #neg(("checked", "T2")),
            ),
            effects=(
                neg(("at", "A1", "T1")),
                ("at", "A1", "T2"),
                ("checked", "T2"),
            )
        ),
    ))
    problem = Problem(
        domain,
        {
            "agent" : ("a", "b"),
            "trashcan" : (-2, -1, 1, 2, 3, 4),
        },

        init=(
            ("startpos", "a", -1),
            ("startpos", "b", -2),
            ("at", "a", -1),
            ("at", "b", -2),
            #neg(("checked", 1)),
            #neg(("checked", 2)),
            #neg(("checked", 3)),
            #neg(("checked", 4)),
        ),

        goal=(
                ("checked", 1),
                ("checked", 2),
                ("checked", 3),
                ("checked", 4),
        )
    )

    def heuristic(state):
        checked_cans = 0
        for p in state.predicates:
            if p[0] == "checked":
                checked_cans += 1
        return checked_cans

    plan = planner(problem, heuristic=heuristic, verbose=verbose)

    if plan is None:
        print("No plan!")
    else:
        for action in plan:
            print(action)

if __name__ == "__main__":
    problem()
