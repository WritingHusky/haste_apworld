from enum import Flag, auto
from typing import NamedTuple, Optional
from BaseClasses import Location, Region


class HasteFlag(Flag):
    # Define flag types for different categories of checks
    Always = auto()
    Boss = auto()
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
    "Shard 10 Boss": HasteLocationData(code=None, flags=HasteFlag.Always),
    "Shard 1 Boss": HasteLocationData(code=1, flags=HasteFlag.Always),
    "Shard 2 Boss": HasteLocationData(code=2, flags=HasteFlag.Always),
    "Shard 3 Boss": HasteLocationData(code=3, flags=HasteFlag.Always),
    "Shard 4 Boss": HasteLocationData(code=4, flags=HasteFlag.Always),
    "Shard 5 Boss": HasteLocationData(code=5, flags=HasteFlag.Always),
    "Shard 6 Boss": HasteLocationData(code=6, flags=HasteFlag.Always),
    "Shard 7 Boss": HasteLocationData(code=7, flags=HasteFlag.Always),
    "Shard 8 Boss": HasteLocationData(code=8, flags=HasteFlag.Always),
    "Shard 9 Boss": HasteLocationData(code=9, flags=HasteFlag.Always),
    "Shard 10 Shop Item": HasteLocationData(code=10, flags=HasteFlag.Always),
    "Shard 1 Shop Item": HasteLocationData(code=11, flags=HasteFlag.Always),
    "Shard 2 Shop Item": HasteLocationData(code=12, flags=HasteFlag.Always),
    "Shard 3 Shop Item": HasteLocationData(code=13, flags=HasteFlag.Always),
    "Shard 4 Shop Item": HasteLocationData(code=14, flags=HasteFlag.Always),
    "Shard 5 Shop Item": HasteLocationData(code=15, flags=HasteFlag.Always),
    "Shard 6 Shop Item": HasteLocationData(code=16, flags=HasteFlag.Always),
    "Shard 7 Shop Item": HasteLocationData(code=17, flags=HasteFlag.Always),
    "Shard 8 Shop Item": HasteLocationData(code=18, flags=HasteFlag.Always),
    "Shard 9 Shop Item": HasteLocationData(code=19, flags=HasteFlag.Always),
    "Ability Slomo": HasteLocationData(code=20, flags=HasteFlag.Always),
    "Ability Grapple": HasteLocationData(code=21, flags=HasteFlag.Always),
    "Ability Fly": HasteLocationData(code=22, flags=HasteFlag.Always),
    # "Ability Slomo": HasteLocationData(code=0, flags=HasteFlag.Always),
    # "Ability Grapple": HasteLocationData(code=1, flags=HasteFlag.Always),
    # "Ability Fly": HasteLocationData(code=2, flags=HasteFlag.Always),
}

# # Per Shard locations
# for i in range(1, 11):
#     LOCATION_TABLE[f"Shard {i} Boss"] = HasteLocationData(
#         code=(9 + i), flags=HasteFlag.Always
#     )  # 10-19
#     LOCATION_TABLE[f"Shard {i} Shop Item"] = HasteLocationData(
#         code=(19 + i), flags=HasteFlag.Always
#     )  # 20-29
