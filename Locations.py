from enum import Flag, auto
from typing import NamedTuple, Optional
from BaseClasses import Location, Region, ItemClassification
from math import floor

from .Items import HasteItem, HasteItemData
from .Regions import SHOP_SEGMENTING, FRAGMENT_SEGMENTING

class HasteFlag(Flag):
    # Define flag types for different categories of checks
    Always = auto()
    Boss = auto()
    PerShardShop = auto()
    GlobalShop = auto()
    PerShardFragment = auto()
    GlobalFragment = auto()
    CaptainsUpgrade = auto()
    Fashion = auto()
    Unknown = auto()


class HasteLocationData(NamedTuple):
    code: Optional[int]
    flags: HasteFlag
    shard: Optional[int] = None
    skin: Optional[int] = None


class HasteLocation(Location):
    game: str = "Haste"

    def __init__(self, player: int, name: str, parent: Region, data: HasteLocationData):

        address = None if data is None else HasteLocation.get_apid(data.code)
        super(HasteLocation, self).__init__(
            player, name, address=address, parent=parent
        )

        self.code = None if data is None else data.code

    @staticmethod
    def get_apid(code: int) -> int:
        base_id: int = 401000
        return base_id + code


LOCATION_TABLE = {
    "Wraith's Hourglass Purchase": HasteLocationData(code=1, flags=HasteFlag.Always),
    "Heir's Javelin Purchase": HasteLocationData(code=2, flags=HasteFlag.Always),
    "Sage's Cowl Purchase": HasteLocationData(code=3, flags=HasteFlag.Always),
}

# Per Shard locations
# IDs 10-19
for i in range(1, 11):
    LOCATION_TABLE[f"Shard {i} Boss"] = HasteLocationData(
        code=9 + i, flags=HasteFlag.Boss, shard=i
    )

# Captain's Upgrade locations
# IDs 20-40
for i in range(1, 5):
    LOCATION_TABLE[f"Captain's Max Health Upgrade Purchase {i}"] = HasteLocationData(
        code=19 + i, flags=HasteFlag.CaptainsUpgrade
    )
LOCATION_TABLE["Captain's Max Lives Upgrade Purchase"] = HasteLocationData(
        code=24, flags=HasteFlag.CaptainsUpgrade
    )
for i in range(1, 5):
    LOCATION_TABLE[f"Captain's Max Energy Upgrade Purchase {i}"] = HasteLocationData(
        code=24 + i, flags=HasteFlag.CaptainsUpgrade
    )
for i in range(1, 7):
    LOCATION_TABLE[f"Captain's Item Rarity Upgrade Purchase {i}"] = HasteLocationData(
        code=30 + i, flags=HasteFlag.CaptainsUpgrade
    )
for i in range(1, 4):
    LOCATION_TABLE[f"Captain's Sparks in Fragments Upgrade Purchase {i}"] = HasteLocationData(
        code=36 + i, flags=HasteFlag.CaptainsUpgrade
    )
for i in range(1, 4):
    LOCATION_TABLE[f"Captain's Starting Sparks Upgrade Purchase {i}"] = HasteLocationData(
        code=39 + i, flags=HasteFlag.CaptainsUpgrade
    )

# Fashion Weeboh Purchase locations
# 41-49
LOCATION_TABLE["Costume Purchase: Crispy"] = HasteLocationData(code=43, flags=HasteFlag.Fashion, skin=1)
LOCATION_TABLE["Costume Purchase: Little Sister"] = HasteLocationData(code=44, flags=HasteFlag.Fashion, skin=2)
LOCATION_TABLE["Costume Purchase: Supersonic Zoe"] = HasteLocationData(code=45, flags=HasteFlag.Fashion, skin=3)
LOCATION_TABLE["Costume Purchase: Zoe the Shadow"] = HasteLocationData(code=46, flags=HasteFlag.Fashion, skin=4)
LOCATION_TABLE["Costume Purchase: Totally Accurate Zoe"] = HasteLocationData(code=47, flags=HasteFlag.Fashion, skin=5)
LOCATION_TABLE["Costume Purchase: Flopsy"] = HasteLocationData(code=48, flags=HasteFlag.Fashion, skin=6)
LOCATION_TABLE["Costume Purchase: Twisted Flopsy"] = HasteLocationData(code=49, flags=HasteFlag.Fashion, skin=7)
LOCATION_TABLE["Costume Purchase: Weeboh"] = HasteLocationData(code=50, flags=HasteFlag.Fashion, skin=10)
LOCATION_TABLE["Costume Purchase: Zoe 64"] = HasteLocationData(code=51, flags=HasteFlag.Fashion, skin=64)

# global shop locations
# IDs 101-200
for j in range(1, 101):
    LOCATION_TABLE[f"Global Shop Item {j:03}"] = HasteLocationData(
        code=100 + j, flags=HasteFlag.GlobalShop, shard=1
    )

# per-shard shop locations
# IDs 201-450
for i in range(1,11):
    for j in range(1, 26):
        LOCATION_TABLE[f"Shard {i} Shop Item {j:02}"] = HasteLocationData(
            code=200 + (i-1)*25 + j, flags=HasteFlag.PerShardShop, shard=i
        )

# global fragment locations
# IDs 451-500
for j in range(1, 51):
    LOCATION_TABLE[f"Global Fragment Clear {j:02}"] = HasteLocationData(
        code=450 + j, flags=HasteFlag.GlobalFragment, shard=1
    )

# per-shard shop locations
# IDs 451-700
for i in range(1,11):
    for j in range(1, 26):
        LOCATION_TABLE[f"Shard {i} Fragment Clear {j:02}"] = HasteLocationData(
            code=500 + (i-1)*25 + j, flags=HasteFlag.PerShardFragment, shard=i
        )

def none_or_within_shard(goal, rpvl, shard) -> bool:
    if shard is None: return True
    if rpvl:
        return (shard <= goal)
    return True

def create_locations(world, regions):


    for location_name, data in LOCATION_TABLE.items():
        if none_or_within_shard(world.options.shard_goal, world.options.remove_post_victory_locations, data.shard):
            if data.flags == HasteFlag.Always or (data.flags == HasteFlag.CaptainsUpgrade and world.options.captains_upgrades == 1):
                location = HasteLocation(world.player, location_name, regions["Menu"], data)
                regions["Menu"].locations.append(location)
            
            # if data.flags == HasteFlag.Fashion and world.options.weeboh_purchases >= 1 and world.options.default_outfit_body != data.skin and world.options.default_outfit_hat != data.skin:
            if data.flags == HasteFlag.Fashion and world.options.weeboh_purchases >= 1:
                location = HasteLocation(world.player, location_name, regions["Menu"], data)
                # Crispy and Twisted Flopsy are unobtainable in the scope of AP with vanilla fashion unlocks
                if world.options.weeboh_purchases == 1:
                    if (data.skin == 1 or data.skin == 7 or data.skin == 2 or data.skin == 3):
                        continue
                    elif data.skin == 10:
                        # adding Weeboh to Shard 5 to piggyback speed calcs
                        location = HasteLocation(world.player, location_name, regions["Shard 5"], data)
                    elif data.skin == 6:
                        # adding Twisted to Shard 7 to piggyback speed calcs
                        location = HasteLocation(world.player, location_name, regions["Shard 7"], data)
                regions["Menu"].locations.append(location)

            if data.flags == HasteFlag.Boss:
                location = HasteLocation(world.player, location_name, regions[f"Shard {data.shard}"], data)
                regions[f"Shard {data.shard}"].locations.append(location)

            if (data.flags == HasteFlag.PerShardShop and world.options.shopsanity == 1) or (data.flags == HasteFlag.GlobalShop and world.options.shopsanity == 2):
                if data.flags == HasteFlag.PerShardShop:
                    shardnum = data.shard
                else:
                    shardnum = 1
                shopnum = int(location_name.split()[-1])
                shoplim = world.options.pershard_shopsanity_quantity if data.flags == HasteFlag.PerShardShop else world.options.global_shopsanity_quantity
                if shopnum <= shoplim:
                    #print(f"shopnum = {shopnum}")
                    # the real item location
                    if shopnum >SHOP_SEGMENTING:
                        regionnum = floor((shopnum-1)/SHOP_SEGMENTING)
                        location = HasteLocation(world.player, location_name, regions[f"Shard {shardnum} Shop {regionnum}"], data)
                        regions[f"Shard {shardnum} Shop {regionnum}"].locations.append(location)
                    else:
                        location = HasteLocation(world.player, location_name, regions[f"Shard {shardnum}"], data)
                        regions[f"Shard {shardnum}"].locations.append(location)
                    # the event item location
                    if shopnum % SHOP_SEGMENTING == 0:
                        regionnum = floor((shopnum-1)/SHOP_SEGMENTING)
                        if shopnum == SHOP_SEGMENTING:
                            regionname = f"Shard {shardnum}"
                        else:
                            regionname = f"Shard {shardnum} Shop {regionnum}"
                        location = HasteLocation(world.player, f"Shard{shardnum}Shop{regionnum}Event", regions[regionname], None)
                        location.place_locked_item(HasteItem(
                            f"Shard{shardnum}ShopRegion{regionnum+1}Unlock",
                            world.player,
                            HasteItemData(f"you cant see me", ItemClassification.progression, None, 1),
                            ItemClassification.progression,
                        ))
                        regions[regionname].locations.append(location)

            if (data.flags == HasteFlag.PerShardFragment and world.options.fragmentsanity == 1) or (data.flags == HasteFlag.GlobalFragment and world.options.fragmentsanity == 2):
                if data.flags == HasteFlag.PerShardFragment:
                    shardnum = data.shard
                else:
                    shardnum = 1
                fragnum = int(location_name.split()[-1])
                fraglim = world.options.pershard_fragmentsanity_quantity if data.flags == HasteFlag.PerShardFragment else world.options.global_fragmentsanity_quantity
                if fragnum <= fraglim:
                    #print(f"fragnum = {fragnum}")
                    # the real item location
                    if fragnum > FRAGMENT_SEGMENTING:
                        regionnum = floor((fragnum-1)/FRAGMENT_SEGMENTING)
                        location = HasteLocation(world.player, location_name, regions[f"Shard {shardnum} Fragmentsanity {regionnum}"], data)
                        regions[f"Shard {shardnum} Fragmentsanity {regionnum}"].locations.append(location)
                        #print(f"    put in Fragmentsanity {regionnum}")
                    else:
                        location = HasteLocation(world.player, location_name, regions[f"Shard {shardnum}"], data)
                        regions[f"Shard {shardnum}"].locations.append(location)
                        #print(f"    put in Shard 1")
                    # the event item location
                    if fragnum % FRAGMENT_SEGMENTING == 0:
                        regionnum = floor((fragnum-1)/FRAGMENT_SEGMENTING)
                        if fragnum == FRAGMENT_SEGMENTING:
                            regionname = f"Shard {shardnum}"
                        else:
                            regionname = f"Shard {shardnum} Fragmentsanity {regionnum}"
                        location = HasteLocation(world.player, f"Shard{shardnum}Fragmentsanity{regionnum}Event", regions[regionname], None)
                        location.place_locked_item(HasteItem(
                            f"Shard{shardnum}Fragmentsanity{regionnum+1}Unlock",
                            world.player,
                            HasteItemData(f"you cant see me", ItemClassification.progression, None, 1),
                            ItemClassification.progression,
                        ))
                        #print(f"    unlock event put in {regionname}")
                        regions[regionname].locations.append(location)