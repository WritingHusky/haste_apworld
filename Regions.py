import typing
from typing import Dict

from BaseClasses import Region, Entrance, MultiWorld



def create_regions(world) -> Dict[str, Region]:
    regions: Dict[str, Region] = {}

    # create initial menu region first
    menu_region = Region(world.origin_region_name, world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)
    regions["Menu"] = menu_region

    # make regions for the 10 shards, each requiring the X-1 number of progressive shards, and each connecting to the menu
    # for fill purposes, there is an arguement to be made that Shard 1 locations should be in the Menu/Initial region, since fill prioritizes spheres 0 & 1 and it takes a 'sphere' to go from menu to shard 1
    s1_region = Region("Shard 1", world.player, world.multiworld)
    connect(world.player, "Shard 1 Entrance", menu_region, s1_region, lambda state: (True))
    regions["Shard 1"] = s1_region

    for i in range (2, 11):
        s2_region = Region(f"Shard {i}", world.player, world.multiworld)
        connect(world.player, f"Shard {i} Entrance", menu_region, s2_region, lambda state, val=i: state.has("Progressive Shard", world.player, val-1))
        regions[f"Shard {i}"] = s2_region
    
    return regions


def connect(player, connection_name, source_region, target_region, rule):
    
    connection = Entrance(player, connection_name, source_region)
    if rule is not None:
        connection.access_rule = rule
    source_region.exits.append(connection)
    connection.connect(target_region)