from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    StartInventoryPool,
    Toggle,
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


@dataclass
class HasteOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for The Wind Waker.
    """

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Logic Settings
    force_reload: ForceReload


haste_option_groups: list[OptionGroup] = [
    OptionGroup(
        "thing Settings",
        [
            ForceReload,
        ],
        start_collapsed=True,
    ),
]
