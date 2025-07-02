from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    StartInventoryPool,
    Toggle,
    Range,
)


# Logic Settings
class ForceReload(Toggle):
    """
    When enabled if you recieve an shard unlock in the hub world, the hub will be forced reloaded
    This includes if you are taking to the captain and other NPC's
    This may cause errors (this is still alpha)
    """

    display_name = "Force Reload"
    default = False

class Shopsanity(Choice):
    """
    Determines how shops are handled, the number of checks per shop is determined by shopsanity_quantity
    Per-Shard: Shops will contain shopsanity_quantity total checks per Shard
    Global: Shops will contain shopsanity_quantity total checks for the entire game, regardless of which Shard you are in
    """

    display_name = "Shopsanity"
    option_off = 0
    option_per_shard = 1
    option_global = 2
    default = option_off


class ShopsanityQuantity(Range):
    """
    Determines how many checks are in each shop.
    """

    display_name = "Shopsanity Quantity"
    range_start = 1
    range_end = 100
    default = 25

@dataclass
class HasteOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for The Wind Waker.
    """

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Logic Settings
    force_reload: ForceReload
    shopsanity: Shopsanity
    shopsanity_quantity: ShopsanityQuantity


haste_option_groups: list[OptionGroup] = [
    OptionGroup(
        "thing Settings",
        [
            ForceReload,
        ],
        start_collapsed=True,
    ),
]
