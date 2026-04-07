from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple, Optional, Union, Any
from random import Random

from BaseClasses import Item, Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import World


class HasteItemData(NamedTuple):
    """
    This class represents the data for an item in Haste

    :param type: The type of the item (e.g., "Item", "Poe").
    :param classification: The item's classification (progression, useful, filler).
    :param code: The unique code identifier for the item.
    :param quantity: The number of this item available.
    """

    type: str
    classification: IC
    code: int
    quantity: int



class HasteItem(Item):
    """
    This class represents an item in Haste

    :param name: The item's name.
    :param player: The ID of the player who owns the item.
    :param data: The data associated with this item.
    :param classification: Optional classification to override the default.
    """

    game: str = "Haste"
    type: Optional[str]

    def __init__(
        self,
        name: str,
        player: int,
        data: HasteItemData,
        classification: Optional[IC] = None,
    ) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else HasteItem.get_apid(data.code),
            player,
        )
        # self.dungeon = dungeon
        self.type = data.type

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 401000
        return base_id + code


def item_factory(
    items: Union[str, Iterable[str]], world: World
) -> Union[HasteItem, list[HasteItem]]:
    """
    Create items based on their names.
    Depending on the input, this function can return a single item or a list of items.

    :param items: The name or names of the items to create.
    :param world: The game world.
    :raises KeyError: If an unknown item name is provided.
    :return: A single item or a list of items.
    """
    if not items:
        pass
    ret: list[HasteItem] = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in ITEM_TABLE:
            ret.append(world.create_item(item))
        else:
            raise KeyError(f"Unknown item {item=}, {items=}")

    return ret[0] if singleton else ret

def parse_perm_quantity(option_value: str, random: Random) -> int:
    """Calculates bound of value for Persistent Item."""
    # function almost entirely stolen from Donkey Kong 64's AP implementation

    try:
        # try to just interpret as an int
        quantity = int(option_value)
        assert 0 <= quantity <= 10 
        return quantity
    except (TypeError, ValueError):
        # else it's the strings
        assert option_value == "random" or len(option_value.split("-")) == 2
        upper_bound = (10 if option_value == "random" else int(option_value.split("-")[1])) + 1
        lower_bound = 1 if option_value == "random" else int(option_value.split("-")[0])
        return random.randrange(lower_bound, upper_bound)


VERY_USEFUL = IC.progression | IC.useful
ITEM_TABLE: dict[str, HasteItemData] = {
    "A New Future": HasteItemData("Victory", IC.progression, 0, 0),
    "Progressive Shard": HasteItemData("Shard", IC.progression, 1, 0),
    "Shard Shop Filler Item": HasteItemData("Filler", IC.filler, 2, 0),
    "Wraith's Hourglass": HasteItemData("Ability", IC.progression, 3, 1),
    "Heir's Javelin": HasteItemData("Ability", IC.progression, 4, 1),
    "Sage's Cowl": HasteItemData("Ability", IC.progression, 5, 1),
    "Anti-Spark 10 bundle": HasteItemData("Anti-Spark Bundle", IC.filler, 6, 0),
    "Anti-Spark 100 bundle": HasteItemData("Anti-Spark Bundle", IC.filler, 7, 0),
    "Anti-Spark 250 bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 8, 0),
    "Anti-Spark 500 bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 9, 0),
    "Anti-Spark 750 bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 10, 0),
    "Anti-Spark 1k bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 11, 0),
    "Wraith": HasteItemData("NPC", IC.progression, 12, 0),
    "Niada": HasteItemData("NPC", IC.progression, 13, 0),
    "Daro": HasteItemData("NPC", IC.progression, 14, 0),
    "The Captain": HasteItemData("NPC", IC.progression, 15, 0),
    "Fashion Weeboh": HasteItemData("NPC", IC.progression, 16, 0),
    "Progressive Speed Upgrade": HasteItemData("Speed", IC.progression, 17, 0),
    "Max Health Upgrade": HasteItemData("Upgrade", IC.useful, 18, 0),
    "Max Lives Upgrade": HasteItemData("Upgrade", IC.useful, 19, 0),
    "Max Energy Upgrade": HasteItemData("Upgrade", IC.useful, 20, 0),
    "Item Rarity Upgrade": HasteItemData("Upgrade", IC.useful, 21, 0),
    "Sparks in Fragments Upgrade": HasteItemData("Upgrade", IC.useful, 22, 0),
    "Starting Sparks Upgrade": HasteItemData("Upgrade", IC.useful, 23, 0),
    "Courier's Board": HasteItemData("Ability", IC.progression, 24, 1),
    "Disaster Trap": HasteItemData("Trap", IC.trap, 25, 0),
    "Landing Downgrade Trap": HasteItemData("Trap", IC.trap, 26, 0),
    "Persistent Common Speed Item": HasteItemData("PermItem", IC.useful, 40, 0),
    "Persistent Common Health Item": HasteItemData("PermItem", IC.useful, 41, 0),
    "Persistent Common Support Item": HasteItemData("PermItem", IC.useful, 42, 0),
    "Persistent Rare Speed Item": HasteItemData("PermItem", IC.useful, 43, 0),
    "Persistent Rare Health Item": HasteItemData("PermItem", IC.useful, 44, 0),
    "Persistent Rare Support Item": HasteItemData("PermItem", IC.useful, 45, 0),
    "Persistent Epic Speed Item": HasteItemData("PermItem", IC.useful, 46, 0),
    "Persistent Epic Health Item": HasteItemData("PermItem", IC.useful, 47, 0),
    "Persistent Epic Support Item": HasteItemData("PermItem", IC.useful, 48, 0),
    "Persistent Legendary Item": HasteItemData("PermItem", IC.useful, 49, 0),
    "Adrenaline": HasteItemData("ItemUnlock", IC.useful, 50, 0),
    "Aromatic Herbs": HasteItemData("ItemUnlock", IC.useful, 51, 0),
    "Atomic Timepiece": HasteItemData("ItemUnlock", IC.useful, 52, 0),
    "BOOSTR POG": HasteItemData("ItemUnlock", IC.useful, 53, 0),
    "Big Pumpkin": HasteItemData("ItemUnlock", IC.useful, 54, 0),
    "Big Spark Magnet": HasteItemData("ItemUnlock", IC.useful, 55, 0),
    "Big Squash": HasteItemData("ItemUnlock", IC.useful, 56, 0),
    "Bitter Herbs": HasteItemData("ItemUnlock", IC.useful, 57, 0),
    "Blood Engine": HasteItemData("ItemUnlock", IC.useful, 58, 0),
    "Boost Remote": HasteItemData("ItemUnlock", IC.useful, 59, 0),
    "Bootleg Pattern": HasteItemData("ItemUnlock", IC.useful, 60, 0),
    "Brittle Breastplate": HasteItemData("ItemUnlock", IC.useful, 61, 0),
    "Charge Boots": HasteItemData("ItemUnlock", IC.useful, 62, 0),
    "Cherry on Top": HasteItemData("ItemUnlock", IC.useful, 63, 0),
    "Clown Shoes": HasteItemData("ItemUnlock", IC.useful, 64, 0),
    "Dangerous Investment Scheme": HasteItemData("ItemUnlock", IC.useful, 65, 0),
    "Delayed Emergency Device": HasteItemData("ItemUnlock", IC.useful, 66, 0),
    "Distance-Based Health Insurance": HasteItemData("ItemUnlock", IC.useful, 67, 0),
    "Dynamo Treadmill": HasteItemData("ItemUnlock", IC.useful, 68, 0),
    "Emergency Shoes": HasteItemData("ItemUnlock", IC.useful, 69, 0),
    "Energy Funnel": HasteItemData("ItemUnlock", IC.useful, 70, 0),
    "Energy Lash": HasteItemData("ItemUnlock", IC.useful, 71, 0),
    "Experimental Autopilot": HasteItemData("ItemUnlock", IC.useful, 72, 0),
    "Experimental Thrusters": HasteItemData("ItemUnlock", IC.useful, 73, 0),
    "Extreme Herbs": HasteItemData("ItemUnlock", IC.useful, 74, 0),
    "Flashback": HasteItemData("ItemUnlock", IC.useful, 75, 0),
    "Fragile Confidence": HasteItemData("ItemUnlock", IC.useful, 76, 0),
    "Fragile Taco": HasteItemData("ItemUnlock", IC.useful, 77, 0),
    "Friendly Looking Star": HasteItemData("ItemUnlock", IC.useful, 78, 0),
    "General Relativity": HasteItemData("ItemUnlock", IC.useful, 79, 0),
    "Golden Necklace": HasteItemData("ItemUnlock", IC.useful, 80, 0),
    "Greed Machine": HasteItemData("ItemUnlock", IC.useful, 81, 0),
    "Growth Potential": HasteItemData("ItemUnlock", IC.useful, 82, 0),
    "Grunt's Helmet": HasteItemData("ItemUnlock", IC.useful, 83, 0),
    "Heart Shaped Mirror": HasteItemData("ItemUnlock", IC.useful, 84, 0),
    "Heir's Determination": HasteItemData("ItemUnlock", IC.useful, 85, 0),
    "High Risk Investment": HasteItemData("ItemUnlock", IC.useful, 86, 0),
    "Impact Activated Healing Drone": HasteItemData("ItemUnlock", IC.useful, 87, 0),
    "Impulse Actived Stabilizer": HasteItemData("ItemUnlock", IC.useful, 88, 0),
    "Instant Compensation Machine": HasteItemData("ItemUnlock", IC.useful, 89, 0),
    "Intangibility": HasteItemData("ItemUnlock", IC.useful, 90, 0),
    "Interest": HasteItemData("ItemUnlock", IC.useful, 91, 0),
    "Jackpot": HasteItemData("ItemUnlock", IC.useful, 92, 0),
    "Karma": HasteItemData("ItemUnlock", IC.useful, 93, 0),
    "Leadership Pipe": HasteItemData("ItemUnlock", IC.useful, 94, 0),
    "Low Grade Timeline Swapper": HasteItemData("ItemUnlock", IC.useful, 95, 0),
    "Momentum Recalibrator": HasteItemData("ItemUnlock", IC.useful, 96, 0),
    "Mortar and Pestle": HasteItemData("ItemUnlock", IC.useful, 97, 0),
    "Mysterious Spring": HasteItemData("ItemUnlock", IC.useful, 98, 0),
    "N-Dimensional-lead Clover": HasteItemData("ItemUnlock", IC.useful, 99, 0),
    "Otherworldly Contact": HasteItemData("ItemUnlock", IC.useful, 100, 0),
    "Overclocked Medical Drone": HasteItemData("ItemUnlock", IC.useful, 101, 0),
    "Overcomplicated Coin": HasteItemData("ItemUnlock", IC.useful, 102, 0),
    "Overwound Pocketwatch": HasteItemData("ItemUnlock", IC.useful, 103, 0),
    "Painful Coil": HasteItemData("ItemUnlock", IC.useful, 104, 0),
    "Pathfinder": HasteItemData("ItemUnlock", IC.useful, 105, 0),
    "Performance Based Health Insurance": HasteItemData("ItemUnlock", IC.useful, 106, 0),
    "Perpetual Motion Machine": HasteItemData("ItemUnlock", IC.useful, 107, 0),
    "Personal Gravity Enhancer": HasteItemData("ItemUnlock", IC.useful, 108, 0),
    "Personal Matter Stabilizer": HasteItemData("ItemUnlock", IC.useful, 109, 0),
    "Planar Reconfiguration": HasteItemData("ItemUnlock", IC.useful, 110, 0),
    "Plutonium Coin": HasteItemData("ItemUnlock", IC.useful, 111, 0),
    "Pocket Snack": HasteItemData("ItemUnlock", IC.useful, 112, 0),
    "Portable Harvester": HasteItemData("ItemUnlock", IC.useful, 113, 0),
    "Protective Medallion": HasteItemData("ItemUnlock", IC.useful, 114, 0),
    "Pungent Herbs": HasteItemData("ItemUnlock", IC.useful, 115, 0),
    "Quick Taco": HasteItemData("ItemUnlock", IC.useful, 116, 0),
    "Recyclable Rocket": HasteItemData("ItemUnlock", IC.useful, 117, 0),
    "Reheated Soup": HasteItemData("ItemUnlock", IC.useful, 118, 0),
    "Replenishing Vial": HasteItemData("ItemUnlock", IC.useful, 119, 0),
    "Restorative Maneuver": HasteItemData("ItemUnlock", IC.useful, 120, 0),
    "Ring Materializer": HasteItemData("ItemUnlock", IC.useful, 121, 0),
    "Risk and Reward": HasteItemData("ItemUnlock", IC.useful, 122, 0),
    "Rocket Boots": HasteItemData("ItemUnlock", IC.useful, 123, 0),
    "Secret Technique Instructions": HasteItemData("ItemUnlock", IC.useful, 124, 0),
    "Shimmering Condenser": HasteItemData("ItemUnlock", IC.useful, 125, 0),
    "Shiny Anchor Pin": HasteItemData("ItemUnlock", IC.useful, 126, 0),
    "Shortcut": HasteItemData("ItemUnlock", IC.useful, 127, 0),
    "Spark Dasher": HasteItemData("ItemUnlock", IC.useful, 128, 0),
    "Spark Furnace": HasteItemData("ItemUnlock", IC.useful, 129, 0),
    "Spark Plug": HasteItemData("ItemUnlock", IC.useful, 130, 0),
    "Spark Powered Propeller": HasteItemData("ItemUnlock", IC.useful, 131, 0),
    "Speedy Recovery": HasteItemData("ItemUnlock", IC.useful, 132, 0),
    "Standard Redirector": HasteItemData("ItemUnlock", IC.useful, 133, 0),
    "Steady Investment": HasteItemData("ItemUnlock", IC.useful, 134, 0),
    "Steel Hat Lining": HasteItemData("ItemUnlock", IC.useful, 135, 0),
    "Tight Schedule": HasteItemData("ItemUnlock", IC.useful, 136, 0),
    "Time Dilation Thing": HasteItemData("ItemUnlock", IC.useful, 137, 0),
    "Timeline Attractor": HasteItemData("ItemUnlock", IC.useful, 138, 0),
    "Timeline Recalibrator": HasteItemData("ItemUnlock", IC.useful, 139, 0),
    "Timeline Refactor": HasteItemData("ItemUnlock", IC.useful, 140, 0),
    "Timeline Shifter": HasteItemData("ItemUnlock", IC.useful, 141, 0),
    "Transition Slingshot": HasteItemData("ItemUnlock", IC.useful, 142, 0),
    "Velocity Powered Syringe": HasteItemData("ItemUnlock", IC.useful, 143, 0),
    "Vitamins": HasteItemData("ItemUnlock", IC.useful, 144, 0),
    "Void Charger": HasteItemData("ItemUnlock", IC.useful, 145, 0),
    "Void Compressor": HasteItemData("ItemUnlock", IC.useful, 146, 0),
    "Well Earned Confidence": HasteItemData("ItemUnlock", IC.useful, 147, 0),
    "Wingspan": HasteItemData("ItemUnlock", IC.useful, 148, 0),
    # TODO: put fashion here
}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    HasteItem.get_apid(data.code): item
    for item, data in ITEM_TABLE.items()
    if data.code is not None
}

# item_name_groups = {
#     "Heart": {
#         "Piece of Heart",
#         "Heart Container",
#     },
#     # "NPC Items": {},
#     # "Shop Items": {},
#     # "Overworld Items": {},
# }
# generic groups, (Name, substring)
# _simple_groups = {
#     ("Swords", "Progressive Master Sword"),
# }
# for basename, substring in _simple_groups:
#     if basename not in item_name_groups:
#         item_name_groups[basename] = set()
#     for itemList in ITEM_TABLE:
#         if substring in itemList:
#             item_name_groups[basename].add(itemList)

# del _simple_groups
