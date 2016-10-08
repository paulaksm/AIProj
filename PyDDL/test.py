#! /usr/bin/env python2
from pyddl import Domain, Action, Problem, neg, planner

# Very simple pathfinding algo.
# The agent starts at 1, and needs to reach 9.

#  1 2 3
#  4 5 6
#  7 8 9


def problem(verbose):
    # problem domain
    domain = Domain((
        # Function to move between tiles.
        Action(
            "move",
            # P1 and P2 are the parameters the solver will tweak.
            parameters=(
                ("agent", "A"),
                ("position", "P1"),
                ("position", "P2"),
            ),
            # Agent(a), Adjacent(P1, P2), At(a, P1), Blank(P2)
            preconditions=(
                ("adjacent", "P1", "P2"),
                ("at", "A", "P1"),
                ("blank", "P2"),
            ),
            # At(a, P2), Blank(P1), not(At(a, P1)), not(Blank(P2))
            effects=(
                ("at", "A", "P2"),
                ("blank", "P1"),
                neg(("at", "A", "P1")),
                neg(("blank", "P2")),
            )
        ),
    ))
    problem = Problem(
        domain,
        {
            # type          values
            "agent": ("a", "b"),
            "position": (1, 2, 3, 4, 5, 6, 7, 8, 9),
        },
        init=(
            # initial KB for our problem
            ("at", "a", 1),
            ("at", "b", 9),
            ("blank", 2),
            ("blank", 3),
            ("blank", 4),
            ("blank", 5),
            ("blank", 6),
            ("blank", 7),
            ("blank", 8),
            ("adjacent", 1, 2),
            ("adjacent", 1, 4),
            ("adjacent", 2, 1),
            ("adjacent", 2, 5),
            ("adjacent", 2, 3),
            ("adjacent", 3, 2),
            ("adjacent", 3, 6),
            ("adjacent", 4, 1),
            ("adjacent", 4, 5),
            ("adjacent", 4, 7),
            ("adjacent", 5, 2),
            ("adjacent", 5, 4),
            ("adjacent", 5, 6),
            ("adjacent", 5, 8),
            ("adjacent", 6, 3),
            ("adjacent", 6, 5),
            ("adjacent", 6, 9),
            ("adjacent", 7, 4),
            ("adjacent", 7, 8),
            ("adjacent", 8, 7),
            ("adjacent", 8, 5),
            ("adjacent", 8, 9),
            ("adjacent", 9, 6),
            ("adjacent", 9, 8),
        ),
        goal=(
            ("at", "a", 9),
            ("at", "b", 1),
        )
    )

    postable = {
                1: (1, 1),
                2: (1, 2),
                3: (1, 3),
                4: (2, 1),
                5: (2, 2),
                6: (2, 3),
                7: (3, 1),
                8: (3, 2),
                9: (3, 3)
    }

    def to_coordinates(state):
        poslist = {}
        for p in state:
            if p[0] == "at":
                poslist[p[1]] = postable[p[2]]
        return poslist

    goal_coords = to_coordinates(problem.goals)

    def manhattan_distance_heuristic(state):
        state_coords = to_coordinates(state.predicates)
        dist = 0
        for k in goal_coords.keys():
            c1, r1 = goal_coords[k]
            c2, r2 = state_coords[k]
            dist += (abs(c1 - c2) + abs(r1 - r2))
        return dist

    plan = planner(problem,
                   heuristic=manhattan_distance_heuristic,
                   verbose=verbose)
    if plan is None:
        print('No Plan!')
    else:
        for action in plan:
            print(action)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)
