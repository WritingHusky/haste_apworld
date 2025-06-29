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
    "Ability Slomo": HasteLocationData(code=0, flags=HasteFlag.Always),
    "Ability Grapple": HasteLocationData(code=1, flags=HasteFlag.Always),
    "Ability Fly": HasteLocationData(code=2, flags=HasteFlag.Always),
}

# Per Shard locations
for i in range(1, 11):
    LOCATION_TABLE[f"Shard {i} Boss"] = HasteLocationData(
        code=9 + i, flags=HasteFlag.Always
    )  # 10-19
    LOCATION_TABLE[f"Shard {i} Shop Item"] = HasteLocationData(
        code=19 + i, flags=HasteFlag.Always
    )  # 20-29
