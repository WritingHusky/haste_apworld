from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    StartInventoryPool,
    Toggle,
    DefaultOnToggle,
    Range,
)


# Logic Settings
class ForceReload(Toggle):
    """
    When enabled if you receive an shard unlock in the hub world, the hub will be forced reloaded
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

class ShardGoal(Range):
    """
    Determines which shard will be the one that contains your victory condition.
    """

    display_name = "Shard Goal"
    range_start = 1
    range_end = 10
    default = 10


class RemovePostVictoryLocations(DefaultOnToggle):
    """
    Removes any locations in shards that happen after the goal set in Shard Goal.
    ex: if Shard Goal is set to 7, this will remove any locations in shards 8, 9, and 10
    """
    
    display_name = "Remove Post-Victory Locations"



class DefaultOutfitBody(Range):
    """
    Sets Zoe's default costume when loading into the game.
    This will not actually unlock the costume from the Fashion Weeboh, and if you change your costume you won't get the "default" back until you reload the game.
    0 = Courier, 1 = Crispy, 2 = Little Sister, 3 = Supersonic Zoe, 4 = Zoe the Shadow
    5 = Totally Accurate Zoe, 6 = Flopsy, 7 = Twisted Flopsy, 8 = Weeboh, 9 = Zoe 64 
    """

    display_name = "Default Outfit Body"
    range_start = 0
    range_end = 9
    default = 0

class DefaultOutfitHat(Range):
    """
    Sets Zoe's default hat when loading into the game.
    This will not actually unlock the hat from the Fashion Weeboh, and if you change your hat you won't get the "default" back until you reload the game.
    0 = Courier, 1 = Crispy, 2 = Little Sister, 3 = Supersonic Zoe, 4 = Zoe the Shadow
    5 = Totally Accurate Zoe, 6 = Flopsy, 7 = Twisted Flopsy, 8 = Weeboh, 9 = Zoe 64 
    """

    display_name = "Default Outfit Hat"
    range_start = 0
    range_end = 9
    default = 0

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
    shard_goal: ShardGoal
    remove_post_victory_locations: RemovePostVictoryLocations
    default_outfit_body: DefaultOutfitBody
    default_outfit_hat: DefaultOutfitHat


haste_option_groups: list[OptionGroup] = [
    OptionGroup(
        "thing Settings",
        [
            ForceReload,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Cosmetic Settings",
        [
            DefaultOutfitBody,
            DefaultOutfitHat
        ],
        start_collapsed=True,
    )
]
