from data import *
from map import *
from xmlrpc.client import boolean

done_borders = []   #Already checked if occupied
calculated_borders = [] #Already called the function on it

can_attack = 6
move_lvl_2 = 4
move_displace_same = 3
move_displace_away = 2
move_lvl_3 = 1

def roads_to_sc(loc):
    armies_number = find_zombie_attack(loc, 3, True, True, loc)
    points = 0
    print(armies_number)
    
    points += move_lvl_3 * armies_number[0][1]
    points += move_displace_away*armies_number[1][3]
    points += move_displace_same*armies_number[1][2]
    points += move_lvl_2*armies_number[1][1]
    points += can_attack*armies_number[2][1]
    
    return points

    
#It returns a list of lists with 4 values each: depth, free movable units, NOT IMPLEMENTED(
#armies that can move after a movement to an adjacent territory by another unit, armies that can move
#after a movement away from the attacking direction of another army)
#It is ordered from highest distance to lowest one
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
    
    borders = DIP[loc][1]
    
    
    ##Prevents going back to territories near the objective
    previous_borders = []
    previous_borders.extend(borders)
    previous_borders.extend(blocked)
        
    armies_number = [4-depth, 0, 0, 0]  #Stores number of army movements
    armies_number_below = []    #Stores results of iterative calls
    
    #Check borders for armies and fleets
    
    not_checked_borders = [item for item in borders if item not in blocked]
    
    for border in not_checked_borders:
        if border in occupied:
            if border not in done_borders:
                if is_army(border) and can_army:
                    armies_number[1] += 1
                elif can_fleet:
                    armies_number[1] += 1
        elif depth > 1:
            temp_armies_below = find_zombie_attack(border, depth-1, can_army, can_fleet, previous_borders)
            armies_number_below = add_to_list(armies_number_below, temp_armies_below)
            calculated_borders.append(border)
            
        done_borders.append(border)
    
    armies_number_below.append(armies_number)
    return armies_number_below

#Returns true if there is an enemy troop in that territory
#Returns false if the army is allied or there is no army
def is_enemy_troop(player, loc):
    for army in armies:
        if army[0] == loc:
            return player == army[1][0]
    return false

def is_enemy_fleet(player, loc):
    for fleet in fleets:
        if army[0] == loc:
            return player == fleet[1][0]
    return false
                    
def add_to_list(original, new):
    if len(original) != len(new):
        original = new.copy()
    else:
        for j in range(len(original)):
            for i in range(1, len(original[j])):
                original[j][i] += new[j][i]
                
    return original

#Returns true if there is an army in the region loc
def is_army(loc):
    army_found = False
    for army in armies:
        if army[0] == loc:
            army_found = True
    
    return army_found