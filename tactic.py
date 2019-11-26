from data import DEFAULT_GERMANY, DEFAULT_ITALY, DEFAULT_RUSSIA, DEFAULT_TURKEY, COLOR_NEUTRAL, DEFAULT_FRANCE
from data import is_land, is_coast_or_sea, find_borders, UNALIGNED, DEFAULT_AUSTRIA, DEFAULT_ENGLAND
from map import land, get, armies, fleets, SUPPLY_CENTERS, occupied, set_color2, write_substitution_image, IMAGE_MAP, \
    color_tactics

done_borders = []   # Already checked if occupied
calculated_borders = []  # Already called the function on it

# Points given to armies at different positions from the considered territory
# 3 level multidecision priorities
sure_attack = 0.44
sure_attack2 = 0.22
can_attack = 0.14
move_lvl_2 = 0.11
move_lvl_3 = 0.09
move_displace_same = 3
move_displace_away = 2


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

def find_army_owner(loc):
    if loc in occupied:
        for army in armies:
            if army[0] == loc:
                return army[1]
    if loc in land:
        return land[loc]
    else:
        for fleet in fleets:
            if fleet[0] == loc:
                return fleet[1]



# Uses the A* algorithm to return the fastest route.
# It returns the reverse list of the path
# If no path can be found it returns an empty list
# Ignore_units allow ignoring units in the map
def find_road(origin, destination, is_fleet, ignore_units):
    open = []
    open_values = []
    close = []
    close_values = []

    # Stores name, g value, h value and parent
    initial = [0, get_distance(origin, destination), '']
    open.append(origin)
    open_values.append(initial)
    found = False

    while not found and len(open) > 0:

        # Find the lowest f value
        lowest = 0
        min = open_values[0][0] + open_values[0][1]
        for i in range(len(open)):
            if open_values[i][0] + open_values[i][1] < min:
                min = open_values[i][0] + open_values[i][1]
                lowest = i

        # Switch the lowest to closed
        close.append(open[lowest])
        del open[lowest]
        close_values.append(open_values[lowest])
        del open_values[lowest]
        if close[-1] == destination:
            found = True
            break

        borders = find_borders(close[-1])
        for border in borders:
            if not (not (border not in close) or not (can_move(border, is_fleet) or (
                    ignore_units and check_land(border, is_fleet)) or border == destination)):
                if border not in open:
                    open.append(border)
                    open_values.append([close_values[-1][0]+1, get_distance(border, destination), close[-1]])

                else:
                    index = open.index(border)
                    if close_values[-1][0] + 1 < open_values[index][0]:
                        # Set new g value and parent
                        open_values[index][0] = close_values[-1][0] + 1
                        open_values[index][2] = close[-1]

    # Finds the reverse path
    path = []
    if found:
        path.append(destination)
        finished = False
        while not finished:
            parent = close_values[close.index(path[-1])][2]
            if parent == origin:
                finished = True
            path.append(parent)

    return path


def can_move(territory, is_fleet):
    if is_army(territory):
        return False
    elif is_coast_or_sea(territory) and is_fleet:
        return True
    elif is_land(territory) and not is_fleet:
        return True
    else:
        return False


def check_land(territory, is_fleet):
    if is_coast_or_sea(territory) and is_fleet:
        return True
    elif is_land(territory) and not is_fleet:
        return True
    else:
        return False


# Get the minimum distance between two territories
def get_distance(origin, destination):
    evaluating = []
    neighbors = []

    evaluating.append(origin)
    count = 0

    while True:
        for territory in evaluating:
            # It ignores the difference amongst coasts
            if territory[:3] == destination[:3]:
                return count
            borders = find_borders(territory)
            for border in borders:
                if border not in neighbors:
                    neighbors.append(border)

        count += 1
        evaluating = neighbors.copy()
        neighbors = []


# Returns true if the territory is a supply center
def is_sc(loc):
    if loc in SUPPLY_CENTERS:
        return True
    else:
        return False


# Returns the numerical superiority in 1 and 2 turns of the enemy, assuming
# all armies move towards the territory
def sure_attacks(loc):
    print(loc)

    owner = find_owner(loc)
    borders = find_borders(loc)
    enemy = 0
    attacks = [0] * 3
    borders2 = []

    if loc in occupied and is_allied_army(loc, owner):
        allied = 1
    else:
        allied = 0

    for border in borders:
        if border in occupied:
            if is_allied_army(border, owner):
                allied += 1
            else:
                enemy += 1
    if enemy > allied:
        # Giving the score to the territory
        attacks[0] = sure_attack*(enemy-allied)

    # Increase the score if the territory is occupied by an enemy
    if loc in occupied and not is_allied_army(loc, owner):
        attacks[0] += sure_attack
        attacks[0] *= 2

    # Increase score if the territory is not defended
    if loc not in occupied:
        attacks[0] *= 1.5
        if enemy == allied and enemy > 0:
            attacks[0] += sure_attack2

    # Finding the second borders
    for border in borders:
        neighbors = find_borders(border)
        for neighbor in neighbors:
            if neighbor is not loc and neighbor not in borders2 and neighbor not in borders:
                borders2.append(neighbor)

    for border in borders2:
        if border in occupied:
            path = find_road(border, loc, not is_army(border), False)
            # Check that the distance is actually 2
            if len(path) == 3:
                if is_allied_army(border, owner):
                    allied += 1
                else:
                    enemy += 1
    if enemy > allied:
        # Giving the score to the territory
        attacks[1] = sure_attack2*(enemy-allied)

    # Yet to complete, does it make sense to only check for single attacks
    # for getting near the territories?
    # If recursive it would work properly?
    # I got to remember which ones have moved somewhere else, might it make sense to
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


def is_allied_army(loc, allies):

    allied = False
    owner = find_army_owner(loc)
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
        attack_score = sure_attacks(loc)
        armies_number = zombie_attack(loc)
        score = 0

        score += attack_score[0]
        score += attack_score[1]
        score += move_lvl_3 * armies_number[2]
        score += move_lvl_2 * armies_number[1]
        score += can_attack * armies_number[0]

        territory_point = [loc, score]

        territory_points.append(territory_point)

    return territory_points


# It returns a list of numbers, meaning how many can attack in the fist turn
# How many in the second and how many in the third
# These are not stacked!!
def zombie_attack(target):
    list_attackers = []
    attackers = [0, 0, 0]
    for territory in occupied:
        if get_distance(territory, target) < 3:
            if is_enemy(find_owner(target), territory) and territory is not target:
                list_attackers.append(territory)

    for territory in list_attackers:
        distance = len(find_road(territory, target, not is_army(territory), False))-1
        if distance == 1:
            attackers[0] += 1
        elif distance == 2:
            attackers[1] += 1
        elif distance == 3:
            attackers[2] += 1

    return attackers


# Returns true if there is an enemy troop in that territory
# Returns false if the army is **allied** or there is no army
def is_enemy(player, loc):
    for army in armies:
        if army[0] == loc:
            return player != army[1]
    for fleet in fleets:
        if fleet[0] == loc:
            return player != fleet[1]
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


# Creates the array of colours for the owner
def owner_color(owner):
    # All territories are set to default color
    for loc in UNALIGNED:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_TURKEY:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_RUSSIA:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_ITALY:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_GERMANY:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_FRANCE:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_ENGLAND:
        set_color2(loc, COLOR_NEUTRAL)
    for loc in DEFAULT_AUSTRIA:
        set_color2(loc, COLOR_NEUTRAL)

    territories = roads_to_sc(owner)
    max = 0
    # Scaling of the score between 0 and 1
    for territory in territories:
        # It's impossible to color the ocean with this image, I should get around making a new one
        if territory[1] > max and is_land(territory[0]):
            max = territory[1]
    for territory in territories:
        territory[1] = territory[1]/max
        # Scaling the values between 0 and 200 for the green values
        green = int(-200*territory[1] + 200)

        # Sets the shade of red of the territory
        # Red is always max, the green dims the color
        if is_land(territory[0]):
            set_color2(territory[0], (255, green, 0))

    write_substitution_image(IMAGE_MAP, owner+'.png', color_tactics)
    return


def tactical_map():
    for owner in ['ENG', 'TUR', 'AUS', 'ITA', 'RUS', 'GER', 'FRA']:
        owner_color(owner)
    return
