from Fill import FillError
from worlds.AutoWorld import World
from .Items import ITEM_TABLE, item_factory
from BaseClasses import ItemClassification as IC, LocationProgressType

ITEM_UNLOCK_ITEMS = [
    "Adrenaline",
    "Aromatic Herbs",
    "Atomic Timepiece",
    "BOOSTR POG",
    "Big Pumpkin",
    "Big Spark Magnet",
    "Big Squash",
    "Bitter Herbs",
    "Blood Engine",
    "Boost Remote",
    "Bootleg Pattern",
    "Brittle Breastplate",
    "Charge Boots",
    "Cherry on Top",
    "Clown Shoes",
    "Dangerous Investment Scheme",
    "Delayed Emergency Device",
    "Distance-Based Health Insurance",
    "Dynamo Treadmill",
    "Emergency Shoes",
    "Energy Funnel",
    "Energy Lash",
    "Experimental Autopilot",
    "Experimental Thrusters",
    "Extreme Herbs",
    "Flashback",
    "Fragile Confidence",
    "Fragile Taco",
    "Friendly Looking Star",
    "General Relativity",
    "Golden Necklace",
    "Greed Machine",
    "Growth Potential",
    "Grunt's Helmet",
    "Heart Shaped Mirror",
    "Heir's Determination",
    "High Risk Investment",
    "Impact Activated Healing Drone",
    "Impulse Actived Stabilizer",
    "Instant Compensation Machine",
    "Intangibility",
    "Interest",
    "Jackpot",
    "Karma",
    "Leadership Pipe",
    "Low Grade Timeline Swapper",
    "Momentum Recalibrator",
    "Mortar and Pestle",
    "Mysterious Spring",
    "N-Dimensional-leaf Clover",
    "Otherworldly Contact",
    "Overclocked Medical Drone",
    "Overcomplicated Coin",
    "Overwound Pocketwatch",
    "Painful Coil",
    "Pathfinder",
    "Performance Based Health Insurance",
    "Perpetual Motion Machine",
    "Personal Gravity Enhancer",
    "Personal Matter Stabilizer",
    "Planar Reconfiguration",
    "Plutonium Coin",
    "Pocket Snack",
    "Portable Harvester",
    "Protective Medallion",
    "Pungent Herbs",
    "Quick Taco",
    "Recyclable Rocket",
    "Reheated Soup",
    "Replenishing Vial",
    "Restorative Maneuver",
    "Ring Materializer",
    "Risk and Reward",
    "Rocket Boots",
    "Secret Technique Instructions",
    "Shimmering Condenser",
    "Shiny Anchor Pin",
    "Shortcut",
    "Spark Dasher",
    "Spark Furnace",
    "Spark Plug",
    "Spark Powered Propeller",
    "Speedy Recovery",
    "Standard Redirector",
    "Steady Investment",
    "Steel Hat Lining",
    "Tight Schedule",
    "Time Dilation Thing",
    "Timeline Attractor",
    "Timeline Recalibrator",
    "Timeline Refactor",
    "Timeline Shifter",
    "Transition Slingshot",
    "Velocity Powered Syringe",
    "Vitamins",
    "Void Charger",
    "Void Compressor",
    "Well Earned Confidence",
    "Wingspan",
]

ACTIVE_ITEM_UNLOCK_ITEMS = {
    "Blood Engine",
    "Boost Remote",
    "Energy Lash",
    "Experimental Autopilot",
    "Mysterious Spring",
    "Otherworldly Contact",
    "Personal Gravity Enhancer",
    "Personal Matter Stabilizer",
    "Portable Harvester",
    "Recyclable Rocket",
    "Replenishing Vial",
    "Rocket Boots",
    "Spark Dasher",
    "Standard Redirector",
    "Steel Hat Lining",
    "Time Dilation Thing",
    "Timeline Shifter",
}


def choose_item_unlocks(world: "World") -> list[str]:
    if world.options.item_unlock_mode == 0:
        return []

    return [
        item_name
        for item_name in ITEM_UNLOCK_ITEMS
        if world.options.item_unlock_mode != 2 or item_name not in ACTIVE_ITEM_UNLOCK_ITEMS
    ]


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

            # the more rules I add to this, the more I think it could probably be formatted better
            # especially since most items in the table have a base quantity of 0 at this point and it doesn't make sense in this format anymore

            additional_items = 0
            if data.type == "Shard":
                if world.options.remove_post_victory_locations:
                    additional_items = max(world.options.shard_goal - 1 + world.options.extra_shard_items, 1)
                else:
                    additional_items = 9 + world.options.extra_shard_items
            elif data.type == "NPC" and world.options.npc_shuffle == 1:
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
                    case "Max Lives Upgrade":
                        additional_items = 1
                    case "Max Energy Upgrade":
                        additional_items = 4
                    case "Item Rarity Upgrade":
                        additional_items = 6
                    case "Sparks in Fragments Upgrade":
                        additional_items = 3
                    case "Starting Sparks Upgrade":
                        additional_items = 3
            elif data.type == "Ability":
                # remove the ability you start with but keep the rest
                match item:
                    case "Courier's Board":
                        if (world.options.starting_ability == 1): additional_items = -1
                    case "Sage's Cowl":
                        if (world.options.starting_ability == 2): additional_items = -1
                    case "Heir's Javelin":
                        if (world.options.starting_ability == 3): additional_items = -1
                    case "Wraith's Hourglass":
                        if (world.options.starting_ability == 4): additional_items = -1
            elif data.type == "PermItem":
                additional_items = 0
            elif data.type == "ItemUnlock":
                # Item unlocks are selected separately by choose_item_unlocks().
                additional_items = 0

            if (data.quantity + additional_items <= 0): continue

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

    item_unlocks = choose_item_unlocks(world)

    useful_pool.extend(item_unlocks)

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
