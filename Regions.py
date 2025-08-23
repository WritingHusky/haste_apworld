import typing
from typing import Dict
from math import floor

from BaseClasses import Region, Entrance, MultiWorld, CollectionState

# static variable that determines how each shop is segmented region-wise
SHOP_SEGMENTING = 5
FRAGMENT_SEGMENTING = 5

def create_regions(world) -> Dict[str, Region]:

    def has_speed(state: CollectionState, shard) -> bool:
        if world.options.speed_upgrade == 1:
            if shard <= 2:
                return True
            elif shard <= 4:
                return state.has("Progressive Speed Upgrade", player, 1)
            elif shard <= 6:
                return state.has("Progressive Speed Upgrade", player, 2)
            elif shard <= 8:
                return state.has("Progressive Speed Upgrade", player, 3)
            else:
                return state.has("Progressive Speed Upgrade", player, 4)
        else:
            return True


    regions: Dict[str, Region] = {}
    player = world.player

    # create initial menu region first
    menu_region = Region(world.origin_region_name, player, world.multiworld)
    world.multiworld.regions.append(menu_region)
    regions["Menu"] = menu_region

    # make regions for the 10 shards, each requiring the X-1 number of progressive shards, and each connecting to the menu
    # for fill purposes, there is an argument to be made that Shard 1 locations should be in the Menu/Initial region, since fill prioritizes spheres 0 & 1 and it takes a 'sphere' to go from menu to shard 1
    
    for i in range (1, 11):
        shard_region = Region(f"Shard {i}", player, world.multiworld)
        if i == 1:
            connect(player, "Shard 1 Entrance", menu_region, shard_region, lambda state: (True))
            regions["Shard 1"] = shard_region
        else:
            connect(player, f"Shard {i} Entrance", menu_region, shard_region, lambda state, val=i: state.has("Progressive Shard", player, val-1) and has_speed(state, val))
            regions[f"Shard {i}"] = shard_region
        
        #subregions for shops, unlocking at SHOP_SEGMENTING-purchase intervals
        for j in range(1,floor(100/SHOP_SEGMENTING)):
            shop_region = Region(f"Shard {i} Shop {j}", player, world.multiworld)
            # if j == 1:
            #     connect(player, f"Shard {i} Shop Region {j} Entrance", shard_region, shop_region, lambda state: (True))
            # else:
            connect(player, f"Shard {i} Shop Region {j} Entrance", shard_region, shop_region, lambda state, vali=i, valj=j: state.has(f"Shard{vali}ShopRegion{valj}Unlock", player))
            regions[f"Shard {i} Shop {j}"] = shop_region

    for i in range(1, floor(50/FRAGMENT_SEGMENTING)):
        fragment_region = Region(f"Fragmentsanity {i}", player, world.multiworld)
        # if i == 1:
        #     connect(player, f"Fragmentsanity Region {i} Entrance", regions["Shard 1"], fragment_region, lambda state: (True))
        # else:
        connect(player, f"Fragmentsanity Region {i} Entrance", regions["Shard 1"], fragment_region, lambda state, vali=i: state.has(f"Fragmentsanity{vali}Unlock", player))
        regions[f"Fragmentsanity {i}"] = fragment_region
    
    return regions


def connect(player, connection_name, source_region, target_region, rule):
    
    connection = Entrance(player, connection_name, source_region)
    if rule is not None:
        connection.access_rule = rule
    source_region.exits.append(connection)
    connection.connect(target_region)