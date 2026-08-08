import typing
from typing import Dict
from math import floor

from BaseClasses import Region, Entrance, MultiWorld, CollectionState

# static variable that determines how each shop is segmented region-wise
SHOP_SEGMENTING = 5
FRAGMENT_SEGMENTING = 5
# copy of the shard_lengths list because otherwise its a circular import and this is easier to solve
SHARD_LENGTHS = [
    13, # Shard 1
    14, # Shard 2
    15, # Shard 3
    16, # Shard 4
    17, # Shard 5
    18, # Shard 6
    19, # Shard 7
    20, # Shard 8
    21, # Shard 9
    26, # Shard 10
    29, # Disaster Shard 1
    33, # Disaster Shard 2
    33, # Disaster Shard 3
    33, # Disaster Shard 4
]

def create_regions(world) -> Dict[str, Region]:

    def has_speed(state: CollectionState, shard) -> bool:
        if world.options.speed_upgrade == 1:
            if shard <= 2:
                return True
            elif shard <= 4:
                return state.has("Progressive Speed Upgrade", player, 1)
            elif shard <= 6:
                return state.has("Progressive Speed Upgrade", player, 2) and has_an_ability(state)
            elif shard <= 8:
                return state.has("Progressive Speed Upgrade", player, 3) and has_an_ability(state)
            else:
                return state.has("Progressive Speed Upgrade", player, 4) and has_an_ability(state)
        else:
            if shard >= 5:
                return has_an_ability(state)
            return True

    def has_an_ability(state: CollectionState) -> bool:
        return world.options.starting_ability > 0 or state.has("Courier's Board", player, 1) or state.has("Sage's Cowl", player, 1) or state.has("Heir's Javelin", player, 1) or state.has("Wraith's Hourglass", player, 1)

    def has_required_blocker(state: CollectionState, checknum) -> bool:
        if world.options.shopsanity != 2:
            return True
        if checknum <= 2:
            return True

        return state.has("Progressive Global Shop Pack", player, checknum//3)


    regions: Dict[str, Region] = {}
    player = world.player

    # reference initial menu region first
    menu_region = Region(world.origin_region_name, player, world.multiworld)
    regions["Menu"] = menu_region

    # make regions for the 10 shards, each requiring the X-1 number of progressive shards, and each connecting to the menu
    # for fill purposes, there is an argument to be made that Shard 1 locations should be in the Menu/Initial region, since fill prioritizes spheres 0 & 1 and it takes a 'sphere' to go from menu to shard 1
    

    for i in range (1, world.options.shard_goal + 1 if world.options.remove_post_victory_locations else 15):
        # special case to make a Shard 1 region for global checks, but otherwise cull regions that are prior to the starting shard
        if (i < world.options.starting_shard and i > 1): continue

        if world.options.shopsanity == 1:
            # check the scaling
            if world.options.pershard_shopsanity_scaling == 1:
                shoplimit = world.options.pershard_shopsanity_quantity
            else:
                shoplimit = int(((world.options.pershard_shopsanity_dynamic_quantity)/100)*(SHARD_LENGTHS[i-1]//2))
        else:
            shoplimit = world.options.global_shopsanity_quantity

        if world.options.fragmentsanity == 1:
            # check the scaling
            if world.options.pershard_fragmentsanity_scaling == 1:
                fraglimit = world.options.pershard_fragmentsanity_quantity
            else:
                fraglimit = int(((world.options.pershard_fragmentsanity_dynamic_quantity)/100)*(SHARD_LENGTHS[i-1]))
        else:
            fraglimit = world.options.global_fragmentsanity_quantity

        shard_region = Region(f"Shard {i}", player, world.multiworld)
        if i == 1:
            connect(player, "Shard 1 Entrance", menu_region, shard_region, lambda state: (True))
            regions["Shard 1"] = shard_region
        else:
            connect(player, f"Shard {i} Entrance", menu_region, shard_region, lambda state, val=i: state.has("Progressive Shard", player, val-1) and has_speed(state, val))
            regions[f"Shard {i}"] = shard_region
        
        #subregions for shops, unlocking at SHOP_SEGMENTING-purchase intervals
        if (not(world.options.shopsanity == 2 and i > 1)):
            for j in range(1,floor(100/SHOP_SEGMENTING)):
                if (j < 1 + floor(shoplimit/SHOP_SEGMENTING)):
                    shop_region = Region(f"Shard {i} Shop {j}", player, world.multiworld)
                    if (i == 1 and world.options.global_shopsanity_blockers):
                        connect(player, f"Shard {i} Shop Region {j} Entrance", shard_region, shop_region, lambda state, vali=i, valj=j: state.has(f"Shard{vali}ShopRegion{valj}Unlock", player) and has_required_blocker(state, valj))
                    else:
                        connect(player, f"Shard {i} Shop Region {j} Entrance", shard_region, shop_region, lambda state, vali=i, valj=j: state.has(f"Shard{vali}ShopRegion{valj}Unlock", player))
                    regions[f"Shard {i} Shop {j}"] = shop_region

        if (not(world.options.fragmentsanity == 2 and i > 1)):
            for j in range(1, floor(100/FRAGMENT_SEGMENTING)):
                if (j < 1 + floor(fraglimit/FRAGMENT_SEGMENTING)):
                    fragment_region = Region(f"Shard {i} Fragmentsanity {j}", player, world.multiworld)
                    connect(player, f"Shard {i} Fragmentsanity Region {j} Entrance", regions["Shard 1"], fragment_region, lambda state, vali=i, valj=j: state.has(f"Shard{vali}Fragmentsanity{valj}Unlock", player))
                    regions[f"Shard {i} Fragmentsanity {j}"] = fragment_region
    
    return regions


def connect(player, connection_name, source_region, target_region, rule):
    
    connection = Entrance(player, connection_name, source_region)
    if rule is not None:
        connection.access_rule = rule
    source_region.exits.append(connection)
    connection.connect(target_region)