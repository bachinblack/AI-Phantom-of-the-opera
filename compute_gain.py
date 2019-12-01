from collections import defaultdict


# Return value: list of tuples.
# The first element is the total number and the second is the number of suspects
def get_rooms_list(gamestate: dict) -> dict:
    tmp = defaultdict(lambda: [0, 0])

    for ch in gamestate['characters']:
        # Get a count of everyone.
        tmp[ch['position']][0] += 1
        if ch['suspect'] is True:
            # Get only the count of suspects.
            tmp[ch['position']][1] += 1
    return tmp


def get_groups_total(gamestate):
    total = 0
    for room, nbs in get_rooms_list(gamestate).items():
        if nbs[0] == 1 or room == gamestate['shadow']:
            # isolated people are negative
            total -= nbs[1]
        else:
            # grouped people are positive
            total += nbs[1]
    return total


# A 8 gain means half the suspect people will be cleared at the end of the round.
# Returns a number between 0 (bad) and 8 (good)
def inspector_gain(gamestate):
    total = get_groups_total(gamestate)
    # Adding .1 if most people are grouped.
    return 8 - abs(total) if total < 0 else 8 - total + .1


# Trying to compute the ghost gain without knowing where the ghost is.
# It will return the opposite gain from the normal function
# Returns a number between 0 (good) and 8 (bad).
def inspector_ghost_gain(gamestate):
    total = get_groups_total(gamestate)
    # Adding .1 if most people are isolated.
    return abs(total) + .1 if total < 0 else total


# Get the number of grouped and isolated people.
# Then, subtract the number including the ghost with the other one.
# The result will be positive if the ghost is in the biggest list.
# Returns a number from -6 (bad) to 8 (perfect).
def ghost_gain(gamestate) -> int:
    # Little safecheck in case we don't have the ghost pos.
    if 'fantom' not in gamestate:
        return inspector_ghost_gain(gamestate)
    # Get ghost given its color.
    ghost = next((item for item in gamestate['characters'] if item["color"] == gamestate['fantom']), None)

    isolated = 0
    grouped = 0
    room_list = get_rooms_list(gamestate)
    ghost_room = room_list[ghost['position']]
    # Check if the ghost is alone or in a dark room
    is_ghost_isolated = ghost_room[0] == 1 or ghost['position'] == gamestate['shadow']

    for id, nbs in room_list.items():
        if nbs[0] == 1 or id == gamestate['shadow']:
            isolated += nbs[1]
        else:
            grouped += nbs[1]

    if is_ghost_isolated is True:
        # Add .1 if the ghost is in the isolated list.
        return (isolated - grouped) + 0.1
    else:
        return grouped - isolated


########
# TEST #
########

# gamestate = {
#     'shadow': 3,
#     'fantom': 'blue',
#     'characters': [
#         {'position': 2, 'suspect': False},
#         {'position': 2, 'suspect': False},
#         {'position': 2, 'suspect': False},
#         {'position': 5, 'suspect': False},
#         {'position': 5, 'suspect': False},
#         {'position': 3, 'suspect': True},
#         {'position': 5, 'suspect': True},
#         {'position': 5, 'suspect': True}
#     ]
# }

# print("room list")
# print(get_rooms_list(gamestate))
# print(get_groups_total(gamestate))
# print("ghost")
# print(ghost_gain(gamestate))
# print("inspector")
# print(inspector_gain(gamestate))
# print("ghost from inspector view")
# print(inspector_ghost_gain(gamestate))
