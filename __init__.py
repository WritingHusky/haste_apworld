from collections.abc import Mapping
from copy import deepcopy
import json
import os
from typing import Any, ClassVar, Optional

from Fill import fill_restrictive
from BaseClasses import (
    CollectionState,
    Item,
    ItemClassification,
    Location,
    LocationProgressType,
    Region,
)
from BaseClasses import ItemClassification as IC
from BaseClasses import Tutorial
from Options import OptionError, Toggle
from .Itempool import generate_itempool
from .location_rules import set_location_access_rules
from worlds.AutoWorld import WebWorld, World
from .Items import (
    ITEM_TABLE,
    HasteItem,
    HasteItemData,
    item_factory,
)
from .Locations import LOCATION_TABLE, HasteLocation, HasteFlag, HasteLocationData
from .options import haste_option_groups, HasteOptions
from .Regions import create_regions


class HasteWeb(WebWorld):
    """
    This class handles the web interface for Haste.

    The web interface includes the setup guide and the options page for generating YAMLs.
    """

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago Haste software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["WritingHusky"],
        )
    ]
    theme = "grass"
    option_groups = haste_option_groups
    rich_text_options_doc = True


class HasteWorld(World):
    """
    Join Zoe on an adventure in Haste.
    """

    # Currently using can reach region to check for access rules. may update later
    explicit_indirect_conditions = False

    options_dataclass = HasteOptions
    options: HasteOptions

    game: ClassVar[str] = "Haste"
    version = "0.2.2"
    topology_present: bool = True

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: HasteItem.get_apid(data.code)
        for name, data in ITEM_TABLE.items()
        if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: HasteLocation.get_apid(data.code)
        for name, data in LOCATION_TABLE.items()
        if data.code is not None
    }

    # item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    required_client_version: tuple[int, int, int] = (0, 5, 0)

    web: ClassVar[HasteWeb] = HasteWeb()

    origin_region_name: str = "Menu"

    player: int

    progression_pool: list[str]

    def __init__(self, *args, **kwargs):
        super(HasteWorld, self).__init__(*args, **kwargs)

        self.nonprogress_locations: set[str] = set()
        self.progress_locations: set[str] = set()

        self.useful_pool: list[str] = []
        self.filler_pool: list[str] = []
        self.prefill_pool: list[str] = []

        self.invalid_locations: list[str] = []

    def _determine_nonprogress_and_progress_locations(
        self,
    ) -> tuple[set[str], set[str]]:
        """
        Sort locations into non progesssion location and progression locations based on options set.
        """

        def add_flag(option: Toggle, flag: HasteFlag) -> HasteFlag:
            return flag if option else HasteFlag.Always

        options = self.options

        enabled_flags = HasteFlag.Always
        enabled_flags |= HasteFlag.Boss

        # If not all the flags for a location are set, then force that location to have a non-progress item.
        nonprogress_locations: set[str] = set()
        progress_locations: set[str] = set()

        for location, data in LOCATION_TABLE.items():
            if data.flags & enabled_flags == data.flags:
                progress_locations.add(location)
            else:
                nonprogress_locations.add(location)

        assert progress_locations.isdisjoint(nonprogress_locations)

        return nonprogress_locations, progress_locations

    # Start of generation Process -----------------------------------------------------------------------

    # stage_assert_generate() not used currently

    def generate_early(self) -> None:
        """
        Setup things ready for generation.
        """

    def create_regions(self) -> None:
        """
        Create and connect regions for the Haste world.

        This method first creates all the regions and adds the locations to them.
        Then it connects the regions to each other.
        """

        regions = Regions.create_regions(self)
        Locations.create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        self.get_location(f"Shard {self.options.shard_goal} Boss").place_locked_item(
            HasteItem(
                "A New Future",
                self.player,
                HasteItemData("A New Future", ItemClassification.progression, 0, 1),
                ItemClassification.progression,
            )
        )

    def create_items(self) -> None:
        """
        Create the items for the Haste world.
        """
        generate_itempool(self)

    # No more items, locations, or regions can be created past this point

    # set_rules() this is where access rules are set
    def set_rules(self) -> None:
        """
        Set the access rules for the Haste world.
        """
        set_location_access_rules(self)

    def pre_fill(self) -> None:
        """
        Apply special fill rules before the fill stage.
        """
        pass

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output APTP file that is used to randomize the GCI.

        :param output_directory: The output directory for the APTP file.
        """
        pass

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        """
        Fill in additional information text into locations, displayed when hinted.

        :param hint_data: A dictionary of mapping a player ID to a dictionary mapping location IDs to the extra hint
        information text. This dictionary should be modified as a side-effect of this method.
        """
        pass

    # Overides the base classification of an item if not None
    def determine_item_classification(self, name: str) -> IC | None:
        assert isinstance(name, str), f"{name=}"
        assert name in ITEM_TABLE, f"{name=}"

        return None

    def create_item(self, name: str) -> HasteItem:
        """
        Create an item for this world type and player.

        :param name: The name of the item to create.
        :raises KeyError: If an invalid item name is provided.
        """
        assert isinstance(name, str), f"{name=}"
        assert name in ITEM_TABLE, f"{name}"

        return HasteItem(
            name,
            self.player,
            ITEM_TABLE[name],
            self.determine_item_classification(name),
        )

    def get_filler_item_name(self) -> str:
        """
        This method is called when the item pool needs to be filled with additional items to match the location count.

        :return: The name of a filler item from this world.
        """
        # If there are still useful items to place, place those first.
        if len(self.useful_pool) > 0:
            return self.useful_pool.pop()

        # If there are still vanilla filler items to place, place those first.
        if len(self.filler_pool) > 0:
            return self.filler_pool.pop()

        assert len(self.useful_pool) == 0
        assert len(self.filler_pool) == 0

        # Use the same weights for filler items used in the base randomizer.
        filler_consumables = [
            "Anti-Spark 10 bundle",
            "Anti-Spark 100 bundle",
            "Anti-Spark 250 bundle",
            "Anti-Spark 500 bundle",
            "Anti-Spark 750 bundle",
            "Anti-Spark 1k bundle",
        ]
        filler_weights = [
            15, #10
            10,  # 100
            5,  # 250
            2,  # 500
            2,  # 750
            1,  # 1k
        ]
        assert len(filler_consumables) == len(
            filler_weights
        ), f"{len(filler_consumables)=}, {len(filler_weights)=}"
        return self.multiworld.random.choices(
            filler_consumables, weights=filler_weights, k=1
        )[0]

    def get_pre_fill_items(self) -> list[Item]:
        """
        Return items that need to be collected when creating a fresh `all_state` but don't exist in the multiworld's
        item pool.

        :return: A list of pre-fill items.
        """
        pre_fiill_items = item_factory(self.prefill_pool, self)
        if pre_fiill_items:
            assert isinstance(pre_fiill_items, list)
        return pre_fiill_items

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data = {
            "Version": self.version,
            "DeathLink": self.options.death_link.value,
            "ForceReload": self.options.force_reload.value,
            "Shard Goal": self.options.shard_goal.value,
            "Shard Unlock Order": self.options.shard_unlock_order.value,
            "Shopsanity": self.options.shopsanity.value,
            "Per-Shard Shopsanity Quantity": self.options.pershard_shopsanity_quantity.value,
            "Global Shopsanity Quantity": self.options.global_shopsanity_quantity.value,
            "Fragmentsanity": self.options.fragmentsanity.value,
            "Fragmentsanity Distribution": self.options.fragmentsanity_distribution.value,
            "Per-Shard Fragmentsanity Quantity": self.options.pershard_fragmentsanity_quantity.value,
            "Global Fragmentsanity Quantity": self.options.global_fragmentsanity_quantity.value,
            "Linear Fragmentsanity Rate": self.options.fragmentsanity_linear_rate.value,
            "NPC Shuffle": self.options.npc_shuffle.value,
            "Captain's Upgrades": self.options.captains_upgrades.value,
            "Speed Upgrades": self.options.speed_upgrade.value,
            "Remove Post-Victory Locations": self.options.remove_post_victory_locations.value,
            "Default Outfit Body": self.options.default_outfit_body.value,
            "Default Outfit Hat": self.options.default_outfit_hat.value,
        }

        return slot_data

    def collect_item(
        self, state: "CollectionState", item: "Item", remove: bool = False
    ) -> Optional[str]:
        """
        Collect an item name into state. For speed reasons items that aren't logically useful get skipped.
        Collect None to skip item.
        :param state: CollectionState to collect into
        :param item: Item to decide on if it should be collected into state
        :param remove: indicate if this is meant to remove from state instead of adding.
        """
        # Adding non progession items that are useful for logic (Non progression IC but used in logic (Trying to cut down on item count))
        if item.advancement:
            return item.name
        return None
