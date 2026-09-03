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
    parse_perm_quantity
)
from .Locations import LOCATION_TABLE, HasteLocation, HasteFlag, HasteLocationData, SHARD_LENGTHS
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
            ["JXJacob", "WritingHusky"],
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
    version = "0.5.1"
    topology_present: bool = True

    perm_item_dict: dict[str, int] = {}

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

    # with open("hastelocations.txt", "w") as f:
    #     for line in location_name_to_id:
    #         print(line, file=f)

    # with open("donkitems.txt", "w") as f:
    #     print(item_name_to_id, file=f)

    # item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    def get_shard_locations(shardnum) -> str:
        res = set()
        for location_name in LOCATION_TABLE.items():
            if location_name[0].startswith(f"Shard {shardnum} "):
                res.add(location_name[0])
        return res

    def get_disaster_shard_locations(shardnum) -> str:
        res = set()
        for location_name in LOCATION_TABLE.items():
            if location_name[0].startswith(f"Disaster Shard {shardnum} "):
                res.add(location_name[0])
        return res
    
    def get_global_locations() -> str:
        res = set()
        for location_name in LOCATION_TABLE.items():
            if location_name[0].startswith("Global "):
                res.add(location_name[0])
        return res
    
    def get_captain_locations() -> str:
        res = set()
        for location_name in LOCATION_TABLE.items():
            if location_name[0].startswith("Captain's "):
                res.add(location_name[0])
        return res
    
    def get_costume_locations() -> str:
        res = set()
        for location_name in LOCATION_TABLE.items():
            if location_name[0].startswith("Costume Purchase:"):
                res.add(location_name[0])
        return res
    
    def get_ability_locations() -> str:
        res = set()
        abilities = ["Wraith's Hourglass Purchase","Heir's Javelin Purchase","Sage's Cowl Purchase"]
        for location_name in abilities:
            if location_name in LOCATION_TABLE:
                res.add(location_name)
        return res

    location_name_groups = {
        "Shard 1": get_shard_locations(1),
        "Shard 2": get_shard_locations(2),
        "Shard 3": get_shard_locations(3),
        "Shard 4": get_shard_locations(4),
        "Shard 5": get_shard_locations(5),
        "Shard 6": get_shard_locations(6),
        "Shard 7": get_shard_locations(7),
        "Shard 8": get_shard_locations(8),
        "Shard 9": get_shard_locations(9),
        "Shard 10": get_shard_locations(10),
        "Disaster Shard 1": get_disaster_shard_locations(1),
        "Disaster Shard 2": get_disaster_shard_locations(2),
        "Disaster Shard 3": get_disaster_shard_locations(3),
        "Disaster Shard 4": get_disaster_shard_locations(4),
        "Global Locations": get_global_locations(),
        "Captain's Purchases": get_captain_locations(),
        "Costume Purchases": get_costume_locations(),
        "Ability Purchases": get_ability_locations(),
    }

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
        # parse persistent item quantities
        if (self.options.persistent_items > 0):
            for name, value in self.options.persistent_item_quantities.items():
                self.perm_item_dict[name] = parse_perm_quantity(value, self.random)

        # imcompatible settings calculations

        # the goal cannot be before the start
        if (self.options.starting_shard > self.options.shard_goal):
            raise OptionError("Shard Goal cannot be lower than the Starting Shard")

        # forbid extra progression items if neither filler check options are enabled
        if (self.options.speed_upgrade or self.options.npc_shuffle or self.options.persistent_items) and (self.options.shopsanity == 0 and self.options.fragmentsanity == 0):
            raise OptionError("In order to enable Speed Upgrades, Shuffled NPCs, or Persistent Items, you must enable either Shopsanity or Fragmentsanity")

        # one sanity needs to be enabled to have a 1-shard-lengthed seed
        if (self.options.shard_goal == self.options.starting_shard):
            if (self.options.shopsanity == 0 and self.options.fragmentsanity == 0):
                raise OptionError("In order to have a Shard Goal equal to your Starting Shard, you must enable either Shopsanity or Fragmentsanity")

        # triangular dist will make the game take a truly absurd amount of time, so limit it to Global or Static Per-Shard
        if (self.options.fragmentsanity == 1 and self.options.fragmentsanity_distribution == 4 and self.options.pershard_fragmentsanity_scaling == 2):
            raise OptionError("Triangular Distribution cannot be enabled with Dynamic Per-Shard scaling due to the risk of inflating the expected playtime of the seed to 20+ hours for just ONE late-game Shard (let alone multiple other Shards).\nIf you wish to play with Triangular Distribution, please switch to either Global Fragmentsanity or Static Per-Shard scaling.")

        worry_about_speed = False
        worry_about_ablity = False
        if (self.options.starting_shard % 2 == 0 and self.options.starting_shard < 9 and not self.options.remove_post_victory_locations):
            # even-numbered starting shards with RPVL will need to worry about having enough mid-shard locations to fit both a Shard and a Speed Upgrade
            worry_about_speed = True
            if (self.options.starting_shard == 4 and self.options.starting_ability == 0):
                # shard 4 specifically also has issues where it'll need an ability to reach Shard 5
                worry_about_ablity = True

        # logic expects an ability starting in Shard 5, so one must be in the starting inventory
        if (self.options.starting_ability == 0 and self.options.starting_shard > 4):
            raise OptionError("In order to have a Starting Shard greater than 4, you must start with an ability")

        # do a more precise count, just to make ABSOLUTELY sure there's enough room
        running_locs = ((self.options.shard_goal) if self.options.remove_post_victory_locations else 14) - (self.options.starting_shard)
        available_shards = running_locs + 1
        running_locs += 3 # add the ability puchases afterwards
        running_items = max(14 if not self.options.remove_post_victory_locations else self.options.shard_goal, 1) + self.options.extra_shard_items - self.options.starting_shard
        # print(f"INIT1   items: {running_items} locs: {running_locs}")
        running_items += 3 if self.options.starting_ability > 0 else 4 # 3 abilities in the pool if you start with one, otherwise 4
        if (self.options.npc_shuffle):
            running_items += 5
            if not self.options.weeboh_purchases > 0: running_items -= 1

        # print(f"INIT2   items: {running_items} locs: {running_locs}")

        if (self.options.speed_upgrade):
            running_items += 6
            if (self.options.starting_shard > 2): running_items -= 1
            if (self.options.starting_shard > 4): running_items -= 1
            if (self.options.starting_shard > 6): running_items -= 1
            if (self.options.starting_shard > 8): running_items -= 1
        else:
            worry_about_speed = False

        # print(f"SPEED   items: {running_items} locs: {running_locs}")

        # adds all persistent items to count
        if (self.options.persistent_items > 0):
            for name, num in self.perm_item_dict.items():
                running_items += num
        
        # print(f"PERSI   items: {running_items} locs: {running_locs}")

        if (self.options.global_shopsanity_blockers > 0 and self.options.shopsanity == 2):
            running_items += ((self.options.global_shopsanity_quantity - 1)//15) + self.options.global_shopsanity_blocker_buffer

        worried_sphere_0 = 0

        if (self.options.fragmentsanity == 1):
            if self.options.pershard_fragmentsanity_scaling == 1:
                worried_sphere_0 += self.options.pershard_fragmentsanity_quantity
                running_locs += available_shards * self.options.pershard_fragmentsanity_quantity
                # print(f"FRAGA   items: {running_items} locs: {running_locs}")
            else:
                for i in range(self.options.starting_shard, self.options.shard_goal+1 if self.options.remove_post_victory_locations else 15):
                    if (i == self.options.starting_shard): worried_sphere_0 += (int)(SHARD_LENGTHS[i-1]*(self.options.pershard_fragmentsanity_dynamic_quantity/100))
                    running_locs += (int)(SHARD_LENGTHS[i-1]*(self.options.pershard_fragmentsanity_dynamic_quantity/100))
                    # print(f"FRAG{i}   items: {running_items} locs: {running_locs}")
        elif (self.options.fragmentsanity == 2): 
            worried_sphere_0 += self.options.global_fragmentsanity_quantity
            running_locs += self.options.global_fragmentsanity_quantity
            # print(f"FRAGG   items: {running_items} locs: {running_locs}")

        if (self.options.shopsanity == 1):
            if self.options.pershard_shopsanity_scaling == 1:
                worried_sphere_0 += self.options.pershard_shopsanity_quantity
                running_locs += available_shards * self.options.pershard_shopsanity_quantity
                # print(f"SHOPA   items: {running_items} locs: {running_locs}")
            else:
                for i in range(self.options.starting_shard, self.options.shard_goal+1 if self.options.remove_post_victory_locations else 15):
                    if (i == self.options.starting_shard): worried_sphere_0 += (int)((SHARD_LENGTHS[i-1]//2)*(self.options.pershard_shopsanity_dynamic_quantity/100))
                    running_locs += (int)((SHARD_LENGTHS[i-1]//2)*(self.options.pershard_shopsanity_dynamic_quantity/100))
                    # print(f"SHOP{i}   items: {running_items} locs: {running_locs}")
        elif (self.options.shopsanity == 2):
            worried_sphere_0 += self.options.global_shopsanity_quantity
            running_locs += self.options.global_shopsanity_quantity
            # print(f"SHOPG   items: {running_items} locs: {running_locs}")

        reqLocs = 3 if worry_about_ablity and worry_about_speed else 2
        # print(f"s: {worry_about_speed} a {worry_about_ablity}")
        # print(f"w: {worried_sphere_0} r: {reqLocs}")
        # you could hypothetically get the god-route of non-NPC shuffle + Shard on check 1 and then buy the items, but omg please just choose less restrictive settings
        if ((worry_about_speed or worry_about_ablity) and worried_sphere_0 < reqLocs):
            raise OptionError(f"Insufficient sphere 0 locations to fit both a Progressive Shard{'' if self.options.starting_shard != 4 else ', an Ability,'} and a Speed Upgrade. Please enable settings that add more locations.")

        if (self.options.weeboh_purchases > 0):
            if (self.options.weeboh_purchases == 1):
                running_locs += 7
            elif (self.options.weeboh_purchases >= 2):
                running_locs += 9
            if self.options.shard_goal < 5 or not self.options.remove_post_victory_locations: running_locs -= 1 # remove weeboh
            if self.options.shard_goal < 7 or not self.options.remove_post_victory_locations: running_locs -= 1 # remove flopsy
            if self.options.shard_goal < 11 or not self.options.remove_post_victory_locations: running_locs -= 1 # remove cripsy
            if self.options.shard_goal < 12 or not self.options.remove_post_victory_locations: running_locs -= 1 # remove twisted flopsy

        # captain's upgrades are not considered, as they add just as many useful items as locations

        # print(f"FINAL   items: {running_items} locs: {running_locs}")
        if running_items > running_locs:
            raise OptionError(f"Insufficient locations ({running_locs}) to fit required items ({running_items}). Please enable settings that add more locations.")

    def create_regions(self) -> None:
        """
        Create and connect regions for the Haste world.

        This method first creates all the regions and adds the locations to them.
        Then it connects the regions to each other.
        """

        regions = Regions.create_regions(self)
        Locations.create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        self.get_location(f"Shard {self.options.shard_goal} Boss" if self.options.shard_goal <=10 else f"Disaster Shard {self.options.shard_goal - 10} Boss").place_locked_item(
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

        # sparks are the default filler at 100% filler, and each other trap subtracts from it
        spark_weight =  100 - self.options.disaster_trap_weight - self.options.landing_trap_weight
        if spark_weight < 0: spark_weight = 0

        round1_weights = [
            self.options.disaster_trap_weight,
            self.options.landing_trap_weight,
            spark_weight
        ]
        round1_items = [
            "Disaster Trap",
            "Landing Downgrade Trap",
            "Anti-Spark"
        ]

        round1 = self.multiworld.random.choices(round1_items, weights=round1_weights, k=1)[0]
        # if the first selection is a trap, return the trap name as-is, else do a second round of weights to decide/return the quality of the anti-spark bundle
        if round1 != "Anti-Spark":
            return round1
        else:
            filler_consumables = [
                "Anti-Spark 10 bundle",
                "Anti-Spark 100 bundle",
                "Anti-Spark 250 bundle",
                "Anti-Spark 500 bundle",
                "Anti-Spark 750 bundle",
                "Anti-Spark 1k bundle",
            ]
            if (self.options.antispark_filler == 0):
                filler_weights = [
                    35, # 10
                    20, # 100
                    2,  # 250
                    2,  # 500
                    1,  # 750
                    1,  # 1k
                ]
            elif (self.options.antispark_filler == 1):
                filler_weights = [
                    15, # 10
                    10, # 100
                    5,  # 250
                    2,  # 500
                    2,  # 750
                    1,  # 1k
                ]
            elif (self.options.antispark_filler == 2):
                filler_weights = [
                    10, # 10
                    5,  # 100
                    5,  # 250
                    2,  # 500
                    2,  # 750
                    2,  # 1k
                ]
            else:
                filler_weights = [
                    5,  #10
                    5,  # 100
                    5,  # 250
                    3,  # 500
                    3,  # 750
                    3,  # 1k
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
            "Starting Shard": self.options.starting_shard.value,
            "Shard Unlock Order": self.options.shard_unlock_order.value,
            "Remove Post-Victory Locaitons": self.options.remove_post_victory_locations.value,
            "Extra Shard Items": self.options.extra_shard_items.value,
            "Shopsanity": self.options.shopsanity.value,
            "Per-Shard Shopsanity Quantity": self.options.pershard_shopsanity_quantity.value,
            "Per-Shard Shopsanity Dynamic Quantity": self.options.pershard_shopsanity_dynamic_quantity.value,
            "Per-Shard Shopsanity Scaling": self.options.pershard_shopsanity_scaling.value,
            "Global Shopsanity Quantity": self.options.global_shopsanity_quantity.value,
            "Global Shopsanity Blockers": self.options.global_shopsanity_blockers.value,
            "Shopsanity Separate": self.options.shopsanity_separate.value,
            "Shopsanity Separate Rate": self.options.shopsanity_separate_rate.value,
            "Fragmentsanity": self.options.fragmentsanity.value,
            "Fragmentsanity Distribution": self.options.fragmentsanity_distribution.value,
            "Per-Shard Fragmentsanity Quantity": self.options.pershard_fragmentsanity_quantity.value,
            "Global Fragmentsanity Quantity": self.options.global_fragmentsanity_quantity.value,
            "Per-Shard Fragmentsanity Dynamic Quantity": self.options.pershard_fragmentsanity_dynamic_quantity.value,
            "Per-Shard Fragmentsanity Scaling": self.options.pershard_fragmentsanity_scaling.value,
            "Linear Fragmentsanity Rate": self.options.fragmentsanity_linear_rate.value,
            "NPC Shuffle": self.options.npc_shuffle.value,
            "Captain's Upgrades": self.options.captains_upgrades.value,
            "Fashion Weeboh's Purchases": self.options.weeboh_purchases.value,
            "Speed Upgrades": self.options.speed_upgrade.value,
            "Starting Ability": self.options.starting_ability.value,
            "Persistent Items": self.options.persistent_items.value, # thank god the mod doesnt need the exact quantities or i'd die
            "Remove Post-Victory Locations": self.options.remove_post_victory_locations.value,
            "Default Outfit Body": self.options.default_outfit_body.value,
            "Default Outfit Hat": self.options.default_outfit_hat.value,
            "Anti-Spark Filler": self.options.antispark_filler.value,
            "Disaster Trap Weight": self.options.disaster_trap_weight.value,
            "Landing Downgrade Trap Weight": self.options.landing_trap_weight.value,
            "Unlock All Items": self.options.unlock_all_items.value,
            "Refund Unnecessary Purchases": self.options.refund_purchases.value,
            "Remove Shop Items When Done": self.options.remove_when_done.value,
            "Scout Locations": self.options.scout_locations.value,
            "Global Disaster Level": self.options.global_disaster_level.value
            # "S-Rank Bonus": self.options.s_rank_bonus.value
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
