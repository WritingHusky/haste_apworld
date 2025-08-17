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


class Fragmentsanity(Choice):
    """
    Determines how checks are distributed when completing fragments
    Linear: Checks are given out every X checks as determined by linear_fragmentsanity_rate
    Balanced Triangular: Checks are given out following a halved triangular distribution, capped at 10 fragments between checks
        Check 10: 26 clears -- Check 20: 101 clears -- Check 30: 205 clears -- Check 40: 305 clears -- check 50: 405 clears
    Triangular: Checks are given out following a triangular distribution. NOT RECOMMENDED FOR SYNCS.
        Check 10: 55 clears -- Check 20: 210 clears -- Check 30: 465 clears -- Check 40: 820 clears -- check 50: 1275 clears
    """

    # Triangular Half: Checks are given out following a halved triangular distribution
    #   Check 10: 26 clears -- Check 20: 101 clears -- Check 30: 226 clears -- Check 40: 401 clears -- check 50: 626 clears

    display_name = "Fragmentsanity"
    option_off = 0
    option_linear = 1
    # option_triangular_half = 2
    option_balanced_triangular = 3
    option_triangular = 4
    default = option_linear

class FragmentsanityQuantity(Range):
    """
    Determines how many checks are tied to completing fragments.
    """

    display_name = "Fragmentsanity Quantity"
    range_start = 1
    range_end = 50
    default = 30

class LinearFragmentsanityRate(Range):
    """
    For linear Fragmentsanity distribution, determines how many fragments must be cleared to send a check
    """

    display_name = "Linear Fragmentsanity Rate"
    range_start = 1
    range_end = 10
    default = 5

class NPCShuffle(Toggle):
    """
    Shuffles Daro, Niada, Wraith, The Captain, and Fashion Weeboh; requiring you to find them before they appear in the hub world.
    """

    display_name = "Hub NPCs"
    default = False

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
    A data class that encapsulates all configuration options for Haste.
    """

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Logic Settings
    force_reload: ForceReload
    shopsanity: Shopsanity
    shopsanity_quantity: ShopsanityQuantity
    fragmentsanity: Fragmentsanity
    fragmentsanity_quantity: FragmentsanityQuantity
    fragmentsanity_linear_rate: LinearFragmentsanityRate
    npc_shuffle: NPCShuffle
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
