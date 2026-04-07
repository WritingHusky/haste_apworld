from dataclasses import dataclass
from Options import (
    Choice,
    OptionDict,
    OptionError,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    StartInventoryPool,
    Toggle,
    DefaultOnToggle,
    Range,
)
from worlds.AutoWorld import World
from BaseClasses import PlandoOptions
import numbers

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
    Determines which Shard will be the one that contains your victory condition.
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

class ExtraShardItems(Range):
    """Determines how many extra Progressive Shards are added into the pool in addition to the ones required to reach your Shard Goal."""

    display_name = "Extra Progressive Shards"
    range_start = 0
    range_end = 20
    default = 0


class RemovePostVictoryLocations(DefaultOnToggle):
    """
    Removes any locations in shards that happen after the goal set in Shard Goal, as well as the Progressive Shard items that would otherwise unlock those Shards.
    ex: if Shard Goal is set to 7, this will have 6 Progressive Shards in the pool and will remove any locations in shards 8, 9, and 10
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
    Determines how Fragmentsanity checks are distributed
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

class StartingAbility(Choice):
    """
    Determines what ability you start with, with the remaining abilities being added as items in the pool.
    Logically, you are expected to have an ability in order to do checks in Shard 5 and beyond.
    """
    display_name = "Starting Ability"
    option_none = 0
    option_couriers_board = 1
    option_wraiths_hourglass = 2
    option_heirs_javelin = 3
    option_sages_cowl = 4
    default = option_couriers_board

class PersistentItems(Choice):
    """
    Determines whether or not Persistent Items are shuffled into the pool.
    Persistent items will be chosen randomly from their corresponding category at the start of a Shard.
    It is recommended that you enable "Unlock All Items" to increase the variety of items seen during a run.
    """

    display_name = "Persistent Items"
    option_off = 0
    option_on = 1
    option_no_active_items = 2
    default = option_off


class ItemUnlockMode(Choice):
    """
    Determines whether or not item unlocks are shuffled into the pool.
    These items are locked at the start of the run and are unlocked as Archipelago checks are collected.

    It is recommended that you enable "Unlock All Items" if you are shuffling item unlocks to avoid confusion with the vanilla unlocks, as this setting overwrites those unlocks in favor of AP unlocks.
    """

    display_name = "Item Unlocks"
    option_off = 0
    option_on = 1
    option_no_active_items = 2
    default = option_off


class PersistentItemQuantity(OptionDict):
    """
    Determines how many of each Persistent Item are added.
    Items are broken up based on Rarity and Category, with the exception of Legendary Items which are their own pool.
    Some items have multiple effects and will thus be present in multiple categories.

    Items are categoriezed as such:
    - Speed: Any item that grants Boost, Speed, spawns a Boost Ring, or grants a special movement option
    - Support: Any item grants Energy, Sparks, Luck, Cooldown reduction, Item retriggers, or Perfect landings
    - Health: Any item that grants Healing, increases Max Health, or grants Invulnerability

    Valid Keys:
    - "common_speed"
    - "common_support"
    - "common_health"
    - "rare_speed"
    - "rare_support"
    - "rare_health"
    - "epic_speed"
    - "epic_support"
    - "epic_health"
    - "legendary"

    Valid Values:
    - a number from 0 to 10 for the key type
    - "random", which will pick a random valid value for you
    - a range in the form "x-y", which will pick a random valid value between x and y
    """

    min = 0
    max_values_dict: dict[str, int] = {
        "common_speed": 10,
        "common_support": 10,
        "common_health": 10,
        "rare_speed": 10,
        "rare_support": 10,
        "rare_health": 10,
        "epic_speed": 10,
        "epic_support": 10,
        "epic_health": 10,
        "legendary": 10,
    }

    # shamelessly stolen verify function from Donkey Kong 64's AP
    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        """Verify Goal Quantity."""
        super(PersistentItemQuantity, self).verify(world, player_name, plando_options)

        for key in self.value.keys():
            if key not in self.max_values_dict.keys():
                raise OptionError(f"{key} is not a valid key for goal_quantity.")

        accumulated_errors = []

        for key, value in self.value.items():
            print(f"Checking {key}: {value}")
            max = self.max_values_dict[key]
            if isinstance(value, numbers.Integral):
                value = int(value)
                if value > max:
                    accumulated_errors.append(f"{key}: {value} is higher than maximum allowed value {max}")
                elif value < self.min:
                    accumulated_errors.append(f"{key}: {value} is lower than minimum allowed value {self.min}")
            else:
                if value == "random":
                    continue
                split = value.split("-")
                if len(split) != 2:
                    accumulated_errors.append(f'{key}: {value} is not an integer or range, nor is it "random".')
                else:
                    for bound in split:
                        try:
                            bound = int(bound)
                        except (ValueError, TypeError):
                            accumulated_errors.append(f'{key}: {value} is not an integer or range, nor is it "random".')
                            continue
                        if bound > max:
                            accumulated_errors.append(f"{key}: Upper edge of range {bound} is higher than maximum allowed value {max}")
                        elif bound < self.min:
                            accumulated_errors.append(f"{key}: Lower edge of range {bound} is lower than minimum allowed value {self.min}")
        print("\n".join(accumulated_errors))
        if accumulated_errors:
            raise OptionError("Found errors with option goal_quantity:\n" + "\n".join(accumulated_errors))
        
    display_name = "Persistent Item Quantities"
    default = {"common_speed": 2, "common_support": 2, "common_health": 2, "rare_speed": 2, "rare_support": 2, "rare_health": 2, "epic_speed": 1, "epic_support": 1, "epic_health": 1, "legendary": 1}


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

    display_name = "Progressive Speed Upgrades"
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

class DisasterTrapWeight(Range):
    """
    Determines the percentage of ALL FILLER that will be converted into Disaster Traps.
    Disaster Traps will add the Disaster Shard Level 1 effects (lava flowers & health loss on low speed) to the current fragment.
    The trap will persist until either the fragment is cleared or Zoe dies, whichever happens first.
    """

    display_name = "Disaster Trap Weight"
    range_start = 0
    range_end = 100
    default = 1

class LandingDowngradeTrapWeight(Range):
    """
    Determines the percentage of ALL FILLER that will be converted into Landing Downgrade Traps.
    Landing Downgrade Traps will "downgrade" any landing performed (Perfect -> Good, Good -> Ok, Ok -> Bad).
    The trap will persist until either the fragment is cleared or Zoe dies, whichever happens first.
    """

    display_name = "Landing Downgrade Trap Weight"
    range_start = 0
    range_end = 100
    default = 1


class UnlockAllItems(Toggle):
    """
    Will unlock all mid-run items at the start of the game, instead of them unlocking gradually as you clear Shards.
    """

    display_name = "Unlock All Items"

# class SRankBonus(Toggle):
#     """
#     When playing Fragmentsanity, any S-Ranks achieved will count as 2 clears instead of 1.
#     Any excess clears do NOT carry over to the next Fragmentsanity check.
#     """

#     display_name = "S-Rank Bonus Fragmentsanity Clear"
    
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
    extra_shard_items: ExtraShardItems
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
    starting_ability: StartingAbility
    permanent_items: PersistentItems
    permanent_item_quantities: PersistentItemQuantity
    item_unlock_mode: ItemUnlockMode
    npc_shuffle: NPCShuffle
    captains_upgrades: CaptainsUpgrades
    weeboh_purchases: FashionWeebohPurchases
    speed_upgrade: PermanentSpeedUpgrades
    force_reload: ForceReload
    antispark_filler: AntisparkFiller
    disaster_trap_weight: DisasterTrapWeight
    landing_trap_weight: LandingDowngradeTrapWeight
    unlock_all_items: UnlockAllItems
    # s_rank_bonus: SRankBonus
    default_outfit_body: DefaultOutfitBody
    default_outfit_hat: DefaultOutfitHat


haste_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Goal Settings",
        [
            ShardGoal,
            ShardUnlockOrder,
            RemovePostVictoryLocations,
            ExtraShardItems
        ],
        start_collapsed=False,
    ),
    OptionGroup(
        "Location Settings",
        [
            Shopsanity,
            ShopsanitySeperate,
            ShopsanitySeperateRate,
            PerShardShopQuantity,
            GlobalShopQuantity,
            Fragmentsanity,
            FragmentsanityDistribution,
            LinearFragmentsanityRate,
            PerShardFragmentQuantity,
            GlobalFragmentQuantity,
            # SRankBonus
        ],
        start_collapsed=False,
    ),
    OptionGroup(
        "Item Settings",
        [
            StartingAbility,
            PermanentSpeedUpgrades,
            PersistentItems,
            PersistentItemQuantity,
            ItemUnlockMode,
            NPCShuffle,
            CaptainsUpgrades,
            FashionWeebohPurchases
        ],
        start_collapsed=False,
    ),
    OptionGroup(
        "Filler Item Settings",
        [
            AntisparkFiller,
            DisasterTrapWeight,
            LandingDowngradeTrapWeight,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "QoL Settings",
        [
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
