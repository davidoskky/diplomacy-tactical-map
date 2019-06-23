from data import is_land, is_coast_or_sea, is_special, find_borders
from map import land, get, armies, fleets, SUPPLY_CENTERS, occupied
done_borders = []   # Already checked if occupied
calculated_borders = []  # Already called the function on it

# Points given to armies at different positions from the considered territory
can_attack = 6
move_lvl_2 = 4
move_displace_same = 3
move_displace_away = 2
move_lvl_3 = 1


# Finds SC and territories with an army of a country
def find_owned(owner):
    owned = find_owned_army(owner)

    for loc in land:
        if get(loc) == owner and is_sc(loc):
            if loc not in owned:
                owned.append(loc)
    return owned


# Returns all territories with an army of the country
def find_owned_army(owner):
    owned = []
    for army in armies:
        if army[1] == owner:
            owned.append(army[0])
    for fleet in fleets:
        if fleet[1] == owner:
            owned.append(fleet[0])
    return owned


# Returns the owner of a territory
def find_owner(loc):
    if loc in land:
        return land[loc]
    else:
        for fleet in fleets:
            if fleet[0] == loc:
                return fleet[1]


# Returns how many moves you have to do from origin
# to reach destination. Returns -1 if it is impossible.
def find_way(origin, destination, can_fleet, can_army, max, steps):
    if steps > max:
        return -1

    if origin == destination:
        return 0

    if is_land(origin) and can_army:
        can_army = True
    else:
        can_army = False

    if is_coast_or_sea(origin) and can_fleet:
        can_fleet = True
    else:
        can_fleet = False

    if not can_army and not can_fleet:
        return -1

    borders = find_borders(origin)

    min = max

    for border in borders:
        result = find_way(border, destination, can_fleet, can_army, min, steps+1)

        if result < min and result >= 0:
            min = result

    if min < max:
        return min+1
    else:
        return -1


# Returns true if the territory is a supply center
def is_sc(loc):
    if loc in SUPPLY_CENTERS:
        return True
    else:
        return False


# Returns the numerical superiority in 1, 2 and 3 turns of the enemy, assuming
# all armies move towards the territory
def sure_attacks(loc):

    owner = find_owner(loc)
    borders = find_borders(loc)
    blocked = []
    free = []
    processing = []
    allied = 1
    enemy = 0
    attacks = [False] * 3

    for border in borders:
        if border in occupied:
            blocked.extend(border)
            if is_allied(border, owner):
                allied += 1
            else:
                enemy += 1
        else:
            free.extend(border)
    if enemy > allied:
        attacks[0] = True

    # Yet to complete, does it make sense to only check for single attacks
    # for getting near the territories?
    # If recursive it would work properly?
    # I got to remember which ones have moved somwhere else, might it make sense to
    # create a new map for every iteration?
    return attacks


# Returns true if the army on the territory is one of
# the players in the allies list
def is_allied(loc, allies):

    allied = False
    owner = find_owner(loc)
    if owner in allies:
        allied = True

    return allied


# Gives a rating to the defendability of all owned territories of a country.
# It is solely based on how many attacks are possible in three turns
# Assuming everyone attacks you and you do not move
def roads_to_sc(owner):
    owned = find_owned(owner)
    territory_points = []
    for loc in owned:
        # We call the zombie attack blocking all the owned SC
        armies_number = find_zombie_attack(loc, 3, True, True, find_owned_army(owner))
        points = 0
        print(armies_number)

        points += move_lvl_3 * armies_number[0][1]
        points += move_displace_away*armies_number[1][3]
        points += move_displace_same*armies_number[1][2]
        points += move_lvl_2*armies_number[1][1]
        points += can_attack*armies_number[2][1]

        territory_point = []
        territory_point.append(loc)
        territory_point.append(points)

        territory_points.append(territory_point)

    return territory_points


# It returns a list of lists with 4 values each: depth, free movable units
# armies that can move after a movement to an adjacent territory by another
# unit, armies that can move
# after a movement away from the attacking direction of another army)
# It is ordered from highest distance to lowest one
def find_zombie_attack(loc, depth, can_army, can_fleet, blocked):
    if depth == 0:
        return

    if is_land(loc) and can_army:
        can_army = True
    else:
        can_army = False

    if is_coast_or_sea(loc) and can_fleet:
        can_fleet = True
    else:
        can_fleet = False

    borders = find_borders(loc)


# Prevents going back to territories near the objective
    previous_borders = []
    previous_borders.extend(borders)
    previous_borders.extend(blocked)

    armies_number = [4-depth, 0, 0, 0]  # Stores number of army movements
    armies_number_below = []    # Stores results of iterative calls

    # Check borders for armies and fleets

    not_checked_borders = [item for item in borders if item not in blocked]

    for border in not_checked_borders:
        if border in occupied:
            # if border not in done_borders:
                if is_army(border) and can_army:
                    armies_number[1] += 1
                elif can_fleet:
                    armies_number[1] += 1
        elif depth > 1:
            temp_armies_below = find_zombie_attack(border, depth-1, can_army, can_fleet, previous_borders)
            armies_number_below = add_to_list(armies_number_below, temp_armies_below)
            calculated_borders.append(border)

        # done_borders.append(border)

    armies_number_below.append(armies_number)
    return armies_number_below


# Returns true if there is an enemy troop in that territory
# Returns false if the army is **allied** or there is no army
def is_enemy(player, loc):
    for army in armies:
        if army[0] == loc:
            return player == army[1]
    for fleet in fleets:
        if army[0] == loc:
            return player == fleet[1]
    return False


def add_to_list(original, new):
    if len(original) != len(new):
        original = new.copy()
    else:
        for j in range(len(original)):
            for i in range(1, len(original[j])):
                original[j][i] += new[j][i]

    return original


# Returns true if there is an army in the region loc
def is_army(loc):
    army_found = False
    for army in armies:
        if army[0] == loc:
            army_found = True

    return army_found
