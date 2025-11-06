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
    When enabled if you receive a Progressive Shard or hub NPC while in the hub world, the hub will be immediately reloaded.
    This may cause weird behaviour if it happens during dialogue with hub NPCs.
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
    default = option_per_shard


class PerShardShopQuantity(Range):
    """
    Determines how many checks are tied to shop purchases for each available Shard.
    """

    display_name = "Per-Shard Shopsanity Quantity"
    range_start = 1
    range_end = 25
    default = 8


class GlobalShopQuantity(Range):
    """
    Determines how many checks are tied to any shop purchase.
    """

    display_name = "Global Shopsanity Quantity"
    range_start = 1
    range_end = 100
    default = 50

class ShopsanitySeperate(DefaultOnToggle):
    """
    For Shopsanity, Archipelago Items will be seperate from normal Haste items bought in shops, purchasing them will send a check.
    If disabled, a check is sent when any item is purchased and dedicated Archipelago Items will not appear in shops.
    """

    display_name = "Shopsanity Items"

class ShopsanitySeperateRate(Range):
    """
    Determines the odds of a shop item being an Archipelago Item as a percentage. Each shop slot is calculated independently. 
    ex: If this value is set to 30, there will be a 30% chance that a single shop item will be an Archipelago Item, and a combined 65% that there will be at least one AP item in a shop.
    """

    display_name = "Shopsanity Item Chance"
    range_start = 1
    range_end = 100
    default = 30

class ShardGoal(Range):
    """
    Determines which shard will be the one that contains your victory condition.
    """

    display_name = "Shard Goal"
    range_start = 1
    range_end = 10
    default = 10

class ShardUnlockOrder(Choice):
    """
    Determines how shards are unlocked when collecting Progressive Shard items.
    Open: Shards will unlock immediately with the required number of Progressive Shards.
    Bosses: Shards will unlock with Progressive Shards + having defeated the previously unlocked Shard's boss.
    """
    option_open = 0
    option_bosses = 1
    default = option_bosses


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
    display_name = "Fragmentsanity"
    option_off = 0
    option_per_shard = 1
    option_global = 2
    default = option_per_shard


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
    default = 15


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
    default = 1

class NPCShuffle(Toggle):
    """
    Shuffles Daro, Niada, Wraith, The Captain, and Fashion Weeboh; requiring you to find them before they can be talked to in the hub world.
    """

    display_name = "Hub NPCs"
    default = False

class CaptainsUpgrades(Toggle):
    """
    Shuffles The Captain's permanent upgrades, and adds their respective purchases from him in the hub as checks.
    All purchases will require 33,250 Anti-Sparks total.
    """

    display_name = "Captain's Upgrades"
    default = False

class FashionWeebohPurchases(Choice):
    """
    Shuffles Fashion Weeboh's costume purchases as checks. Currently does NOT add the costumes themselves as items into the pool.
    All purchases will require 16,500 Anti-Sparks total for Vanilla, or 22,700 for Vanilla Plus or All Unlocks.

    Vanilla: Costume purchases are only available as per their vanilla requirements:
        Little Sister and Supersonic Zoe: Unlocked by default and do not need to be purchased
        Zoe the Shadow and Zoe 64: Available as soon as the Fashion Weeboh is available
        Weeboh: Unlocks after unlocking Shard 5
        Flopsy: Unlocks after unlocking Shard 7
        Totally Accurate Zoe: Unlocks after obtaining all Abilities
        Crispy and Twisted Flopsy: Unobtainable due to their post-game unlock requirements, which are not yet implemented in AP
    Vanilla Plus: The same conditions as above, plus Crispy, Twisted Flopsy, Little Sister, and Supersonic Zoe's purchases are available as soon as the Fashion Weeboh is available.
    All Unlocks: All costume purchases are available as soon as the Fashion Weeboh is available
    """

    display_name = "Fashion Weeboh Purchases"
    option_off = 0
    option_vanilla = 1
    option_vanilla_plus = 2
    option_all_unlocks = 3

class AntisparkFiller(Choice):
    """
    Determines the average value of the Anti-Spark Bundle filler items added into the pool.

    Sparse: Approximately 9,200 Anti-Sparks per 100 filler items
    Standard: Approximately 16,800 Anti-Sparks per 100 filler items
    Plentiful: Approximately 24,500 Anti-Sparks per 100 filler items
    Excessive: Approximately 35,600 Anti-Sparks per 100 filler items
    """

    display_name = "Anti-Spark Filler"
    option_sparse = 0
    option_standard = 1
    option_plentiful = 2
    option_excessive = 3
    default = option_standard

class PermanentSpeedUpgrades(Toggle):
    """
    Reduces Zoe's base run speed to 60%, and adds 6 Speed Upgrades that increase her base run speed by 10% each (totalling 120% run speed with all 6 upgrades)
    Zoe's TOTAL speed includes more than just her BASE run speed; so liberal use of Boost-increasing items, abilities, and good landings will be needed to compensate for this initial reduction
    Shards will require a certain number of speed upgrades to logically complete:
        Shards 1-2: No speed upgrades
        Shards 3-4: 1 speed upgrade
        Shards 5-6: 2 speed upgrades
        Shards 7-8: 3 speed upgrades
        Shards 9-10: 4 speed upgrades
    """

    display_name = "Permanent Speed Upgrades"
    default = False

class DefaultOutfitBody(Choice):
    """
    Sets Zoe's default costume when loading into the game.
    This will not actually unlock the costume from the Fashion Weeboh, and if you change your costume you won't get your chosen outfit back until you reload the game.
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
    This will not actually unlock the hat from the Fashion Weeboh, and if you change your hat you won't get your chosen hat back until you reload the game.
    """
    # This will unlock the costume from the Fashion Weeboh, removing its purchase as a location if playing with Fashion Weeboh Purchases.

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


class UnlockAllItems(Toggle):
    """
    Will unlock all mid-run items at the start of the game, instead of them unlocking gradually as you clear Shards.
    """

    display_name = "Unlock All Items"
    
@dataclass
class HasteOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for Haste.
    """

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Logic Settings
    shard_goal: ShardGoal
    shard_unlock_order: ShardUnlockOrder
    remove_post_victory_locations: RemovePostVictoryLocations
    shopsanity: Shopsanity
    pershard_shopsanity_quantity: PerShardShopQuantity
    global_shopsanity_quantity: GlobalShopQuantity
    shopsanity_seperate: ShopsanitySeperate
    shopsanity_seperate_rate: ShopsanitySeperateRate
    fragmentsanity: Fragmentsanity
    fragmentsanity_distribution: FragmentsanityDistribution
    pershard_fragmentsanity_quantity: PerShardFragmentQuantity
    global_fragmentsanity_quantity: GlobalFragmentQuantity
    fragmentsanity_linear_rate: LinearFragmentsanityRate
    npc_shuffle: NPCShuffle
    captains_upgrades: CaptainsUpgrades
    weeboh_purchases: FashionWeebohPurchases
    speed_upgrade: PermanentSpeedUpgrades
    force_reload: ForceReload
    antispark_filler: AntisparkFiller
    unlock_all_items: UnlockAllItems
    default_outfit_body: DefaultOutfitBody
    default_outfit_hat: DefaultOutfitHat


haste_option_groups: list[OptionGroup] = [
    OptionGroup(
        "QoL Settings",
        [
            AntisparkFiller,
            UnlockAllItems,
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
