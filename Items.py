from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple, Optional, Union

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
    :param item_id: The ID used to represent the item in-game.
    """

    type: str
    classification: IC
    code: Optional[int]
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


VERY_USEFUL = IC.progression | IC.useful
ITEM_TABLE: dict[str, HasteItemData] = {
    "A New Future": HasteItemData("Victory", IC.progression, 0, 0),
    "Progressive Shard": HasteItemData("Shard", IC.progression, 1, 9),
    "Shard Shop Filler Item": HasteItemData("Filler", IC.filler, 2, 0),
    "Slomo": HasteItemData("Ability", IC.progression, 3, 1),
    "Grapple": HasteItemData("Ability", IC.progression, 4, 1),
    "Fly": HasteItemData("Ability", IC.progression, 5, 1),
    "Anti-Spark 10 bundle": HasteItemData("Anti-Spark Bundle", IC.filler, 6, 0),
    "Anti-Spark 100 bundle": HasteItemData("Anti-Spark Bundle", IC.filler, 7, 0),
    "Anti-Spark 250 bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 8, 0),
    "Anti-Spark 500 bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 9, 0),
    "Anti-Spark 750 bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 10, 0),
    "Anti-Spark 1k bundle": HasteItemData("Anti-Spark Bundle", IC.useful, 11, 0),
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
