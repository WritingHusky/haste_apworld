from enum import Flag, auto
from typing import NamedTuple, Optional
from BaseClasses import Location, Region


class HasteFlag(Flag):
    # Define flag types for different categories of checks
    Always = auto()
    Boss = auto()
    PerShardShop = auto()
    GlobalShop = auto()
    Unknown = auto()


class HasteLocationData(NamedTuple):
    code: Optional[int]
    flags: HasteFlag


class HasteLocation(Location):
    game: str = "Haste"

    def __init__(self, player: int, name: str, parent: Region, data: HasteLocationData):

        address = None if data.code is None else HasteLocation.get_apid(data.code)
        super(HasteLocation, self).__init__(
            player, name, address=address, parent=parent
        )

        self.code = data.code

    @staticmethod
    def get_apid(code: int) -> int:
        base_id: int = 401000
        return base_id + code


LOCATION_TABLE = {
    "Ability Slomo": HasteLocationData(code=1, flags=HasteFlag.Always),
    "Ability Grapple": HasteLocationData(code=2, flags=HasteFlag.Always),
    "Ability Fly": HasteLocationData(code=3, flags=HasteFlag.Always),
}

# Per Shard locations
for i in range(1, 11):
    LOCATION_TABLE[f"Shard {i} Boss"] = HasteLocationData(
        code=9 + i, flags=HasteFlag.Boss
    )


# per-shard shop locations
for i in range(1,11):
    for j in range(1, 101):
        LOCATION_TABLE[f"Shard {i} Shop Item {j}"] = HasteLocationData(
            code=100 + i*100 + j, flags=HasteFlag.PerShardShop,
        )

# global shop locations
for j in range(1, 101):
    LOCATION_TABLE[f"Global Shop Item {j}"] = HasteLocationData(
        code=100 + j, flags=HasteFlag.GlobalShop,
    )


def create_locations(world, menu_region):

    # will DEFINITELY need to adjust this once there is more than one region in the game

    for location_name, data in LOCATION_TABLE.items():
        if data.flags == HasteFlag.Always or data.flags == HasteFlag.Boss:
            location = HasteLocation(world.player, location_name, menu_region, data)
            menu_region.locations.append(location)

        if data.flags == HasteFlag.PerShardShop and world.options.shopsanity == 1:
            shopnum = int(location_name.split()[-1])
            if shopnum <= world.options.shopsanity_quantity:
                location = HasteLocation(world.player, location_name, menu_region, data)
                menu_region.locations.append(location)

        if data.flags == HasteFlag.GlobalShop and world.options.shopsanity == 2:
            shopnum = int(location_name.split()[-1])
            if shopnum <= world.options.shopsanity_quantity:
                location = HasteLocation(world.player, location_name, menu_region, data)
                menu_region.locations.append(location)       