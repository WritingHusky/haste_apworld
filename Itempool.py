from Fill import FillError
from worlds.AutoWorld import World
from .Items import ITEM_TABLE, item_factory
from BaseClasses import ItemClassification as IC, LocationProgressType


def generate_itempool(world: "World") -> None:
    multiworld = world.multiworld

    # Get the core pool of items.
    pool, precollected_items = get_pool_core(world)

    # Add precollected items to the multiworld's `precollected_items` list.
    for item in precollected_items:
        multiworld.push_precollected(item_factory(item, world))

    # Create the pool of the remaining shuffled items.
    items = item_factory(pool, world)
    multiworld.random.shuffle(items)

    multiworld.itempool.extend(items)


def get_pool_core(world: "World") -> tuple[list[str], list[str]]:
    pool: list[str] = []
    precollected_items: list[str] = []

    progression_pool: list[str] = []
    useful_pool: list[str] = []
    filler_pool: list[str] = []
    prefill_pool: list[str] = []

    for item, data in ITEM_TABLE.items():
        if isinstance(data.code, int):
            adjusted_classification = world.determine_item_classification(item)
            classification = (
                data.classification
                if adjusted_classification is None
                else adjusted_classification
            )

            # Can do fancy stuff here

            additional_items = 0
            if data.type == "NPC" and world.options.npc_shuffle == 1:
                # add NPCs into the pool
                additional_items = 1
                if world.options.captains_upgrades != 1 and item == "The Captain":
                    # make Captain non-progression if he doesnt have checks
                    classification = IC.useful
                if world.options.weeboh_purchases != 1 and item == "Fashion Weeboh":
                    # make Fashion Weeboh non-progression if they dont have checks
                    classification = IC.filler
            elif data.type == "Speed" and world.options.speed_upgrade == 1:
                # add 6 speed upgrades into the pool
                additional_items = 6
            elif data.type == "Upgrade" and world.options.captains_upgrades == 1:
                match item:
                    case "Max Health Upgrade":
                        additional_items = 4
                    case "Extra Lives Upgrade":
                        additional_items = 1
                    case "Max Engrgy Upgrade":
                        additional_items = 4
                    case "Item Rarity Upgrade":
                        additional_items = 6
                    case "Sparks in Shard Upgrade":
                        additional_items = 3
                    case "Starting Sparks Upgrade":
                        additional_items = 3


            if classification & IC.progression:
                progression_pool.extend([item] * (data.quantity + additional_items))
            elif classification & IC.useful:
                useful_pool.extend([item] * (data.quantity + additional_items))
            else:
                filler_pool.extend([item] * (data.quantity + additional_items))
        else:
            assert False, f"{item=} does not have a code"

    placeable_locations = [
        location
        for location in world.multiworld.get_locations(world.player)
        if location.address is not None and location.item is None
    ]

    num_items_left_to_place = len(placeable_locations) - len(prefill_pool)

    # Check progression pool against locations that can hold progression items
    if len(progression_pool) > len(
        [
            location
            for location in placeable_locations
            if location.progress_type != LocationProgressType.EXCLUDED
        ]
    ):
        raise FillError(
            "There are insufficient locations to place progression items! "
            f"Trying to place {len(progression_pool)} items in only {num_items_left_to_place} locations."
        )

    # world.progression_pool = progression_pool
    pool.extend(progression_pool)
    num_items_left_to_place -= len(progression_pool)

    world.multiworld.random.shuffle(useful_pool)
    world.multiworld.random.shuffle(filler_pool)
    world.useful_pool = useful_pool
    world.filler_pool = filler_pool
    world.prefill_pool = prefill_pool

    # assert len(world.useful_pool) > 0
    # assert len(world.filler_pool) > 0

    # Place filler items ensure that the pool has the correct number of items.
    pool.extend([world.get_filler_item_name() for _ in range(num_items_left_to_place)])
    # pool.extend(filler_pool)

    return pool, precollected_items
