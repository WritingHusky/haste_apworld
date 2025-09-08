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
    Per-Shard: Shops will contain checks that are specific to each Shard
    Global: Shops will contain checks for the entire game, regardless of which Shard you are in
    """

    display_name = "Shopsanity"
    option_off = 0
    option_per_shard = 1
    option_global = 2
    default = option_off


class PerShardShopQuantity(Range):
    """
    Determines how many checks are tied to shop purchases for each available Shard.
    """

    display_name = "Per-Shard Shopsanity Quantity"
    range_start = 1
    range_end = 25
    default = 10


class GlobalShopQuantity(Range):
    """
    Determines how many checks are tied to any shop purchase.
    """

    display_name = "Global Shopsanity Quantity"
    range_start = 1
    range_end = 100
    default = 50

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
    Determines how fragment clears are handled.
    Per-Shard: Fragment clears will have checks that are specific to each Shard
    Global: Fragment clears will have checks for the entire game, regardless of which Shard you are in
    """
    option_off = 0
    option_per_shard = 1
    option_global = 2
    default = option_off


class FragmentsanityDistribution(Choice):
    """
    Determines how fragmentsanity checks are distributed
    Linear: Checks are given out every X checks as determined by linear_fragmentsanity_rate
    Balanced Triangular: Checks are given out following a halved triangular distribution, capped at 10 fragments between checks
        Check 10: 30 clears -- Check 20: 110 clears -- Check 30: 210 clears -- Check 40: 310 clears -- check 50: 410 clears
    Triangular: Checks are given out following a triangular distribution. NOT RECOMMENDED FOR SYNCS.
        Check 10: 55 clears -- Check 20: 210 clears -- Check 30: 465 clears -- Check 40: 820 clears -- check 50: 1275 clears
    """

    # Triangular Half: Checks are given out following a halved triangular distribution
    #   Check 10: 30 clears -- Check 20: 110 clears -- Check 30: 240 clears -- Check 40: 420 clears -- check 50: 650 clears

    display_name = "Fragmentsanity Distribution"
    option_linear = 1
    # option_triangular_half = 2
    option_balanced_triangular = 3
    option_triangular = 4
    default = option_linear

class PerShardFragmentQuantity(Range):
    """
    Determines how many checks are tied to fragment clears for each available Shard.
    """

    display_name = "Per-Shard Fragmentsanity Quantity"
    range_start = 1
    range_end = 25
    default = 10


class GlobalFragmentQuantity(Range):
    """
    Determines how many checks are tied to any fragment clears.
    """

    display_name = "Global Fragmentsanity Quantity"
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
    default = 3

class NPCShuffle(Toggle):
    """
    Shuffles Daro, Niada, Wraith, The Captain, and Fashion Weeboh; requiring you to find them before they can be talked to in the hub world.
    """

    display_name = "Hub NPCs"
    default = False

class PermanentSpeedUpgrades(Toggle):
    """
    Reduces Zoe's base run speed to 60%, and adds 6 Speed Upgrades that increase her base run speed by 10% each (totalling 120% run speed with all 6 upgrades)
    Zoe's TOTAL speed includes more than just her BASE run speed; so liberal use of Boost-increasing items, abilities, and good landings will be needed to compensate for this initial reduction
    Shards will require a certain number of speed upgrades to logically complete:
        Shards 1-2: No speed upgrades
        Shards 3-4: 1 speed upgrade
        Shards 5-7: 2 speed upgrades
        Shards 7-8: 3 speed upgrades
        Shards 9-10: 4 speed upgrades
    """

    display_name = "Permanent Speed Upgrades"
    default = False

class DefaultOutfitBody(Choice):
    """
    Sets Zoe's default costume when loading into the game.
    This will not actually unlock the costume from the Fashion Weeboh, and if you change your costume you won't get the "default" back until you reload the game.
    """

    display_name = "Default Outfit Body"
    option_default = 0
    option_cripsy = 1
    option_little_sister = 2
    option_supersonic_zoe = 3
    option_zoe_the_shadow = 4
    option_totally_accurate_zoe = 5
    option_flopsy = 6
    option_twisted_flopsy = 7
    option_weeboh = 10
    option_zoe_64 = 64
    default = option_default

class DefaultOutfitHat(Choice):
    """
    Sets Zoe's default hat when loading into the game.
    This will not actually unlock the hat from the Fashion Weeboh, and if you change your hat you won't get the "default" back until you reload the game.
    """

    display_name = "Default Outfit Hat"
    option_default = 0
    option_cripsy = 1
    option_little_sister = 2
    option_supersonic_zoe = 3
    option_zoe_the_shadow = 4
    option_totally_accurate_zoe = 5
    option_flopsy = 6
    option_twisted_flopsy = 7
    option_weeboh = 10
    option_zoe_64 = 64
    default = option_default

    
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
    pershard_shopsanity_quantity: PerShardShopQuantity
    global_shopsanity_quantity: GlobalShopQuantity
    fragmentsanity: Fragmentsanity
    fragmentsanity_distribution: FragmentsanityDistribution
    pershard_fragmentsanity_quantity: PerShardFragmentQuantity
    global_fragmentsanity_quantity: GlobalFragmentQuantity
    fragmentsanity_linear_rate: LinearFragmentsanityRate
    npc_shuffle: NPCShuffle
    shard_goal: ShardGoal
    speed_upgrade: PermanentSpeedUpgrades
    remove_post_victory_locations: RemovePostVictoryLocations
    default_outfit_body: DefaultOutfitBody
    default_outfit_hat: DefaultOutfitHat


haste_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Other Settings",
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
