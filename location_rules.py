from typing import Callable
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from .Locations import LOCATION_TABLE, SHARD_LENGTHS


def set_location_access_rules(world: "World"):

    def set_rule_if_exists(
        location_name: str,
        rule: Callable[[CollectionState], bool],
    ) -> None:
        # Only worry about logic if the location can be a progress item (and location_name not in world.nonprogress_locations) do not worry bout yet
        assert location_name in LOCATION_TABLE, f"{location_name=}"
        location = world.get_location(location_name)
        set_rule(location, rule)

    def has_NPC(state: CollectionState, npc) -> bool:
        if world.options.npc_shuffle:
            return state.has(npc, player, 1)
        else:
            return True
        
    def fashion_unlock(state: CollectionState, skin) -> bool:
        if world.options.weeboh_purchases < 3:
            if skin == 10:
                return state.has("Progressive Shard", player, 4)
            elif skin == 6:
                return state.has("Progressive Shard", player, 6)
            elif skin == 1:
                return state.has("Progressive Shard", player, 10)
            elif skin == 7:
                return state.has("Progressive Shard", player, 11)
            elif skin == 5:
                return has_ability(state, "Courier's Board") and has_ability(state, "Sage's Cowl") and has_ability(state, "Heir's Javelin") and has_ability(state, "Wraith's Hourglass")
        return True

    def has_ability(state: CollectionState, ability) -> bool:
        match ability:
            case "Courier's Board":
                return (world.options.starting_ability == 1) or state.has("Courier's Board", player, 1)
            case "Sage's Cowl":
                return (world.options.starting_ability == 4) or state.has("Sage's Cowl", player, 1)
            case "Heir's Javelin":
                return (world.options.starting_ability == 3) or state.has("Heir's Javelin", player, 1)
            case "Wraith's Hourglass":
                return (world.options.starting_ability == 2) or state.has("Wraith's Hourglass", player, 1)
            case _:
                # you shouldnt be here
                return True
    
    def has_purchasable_shards(state: CollectionState, purchasenum) -> bool:
        # calculate How Many Progressive Shards Are There (HMPSAT) in the game, then use it as a cap when trying to calculate the shard buffers
        HMPSAT = ((world.options.shard_goal) if world.options.remove_post_victory_locations else 14) - world.options.starting_shard
        # remove 1 shard from the calcs because 1 buffer is assumed for all calcs anyway
        if (HMPSAT > 0): HMPSAT -= 1
        # if there is literally no available prog shards to gain, just assume its true
        if (HMPSAT == 0): return True
        # also, since the buffers are there to give the player time to do get antisparks, it is calced from the ADDITIONAL shards gained, and ignores starting shards
        match purchasenum:
            case 1 | 2:
                return state.has("Progressive Shard", player, world.options.starting_shard)
            case 3 | 4:
                return state.has("Progressive Shard", player, world.options.starting_shard + min(2, HMPSAT))
            case 5:
                return state.has("Progressive Shard", player, world.options.starting_shard + min(4, HMPSAT))
            case 6:
                return state.has("Progressive Shard", player, world.options.starting_shard + min(7, HMPSAT))
            case _:
                # you shouldnt be here
                return True
            


    player = world.player

    world.multiworld.completion_condition[player] = lambda state: state.has(
        "A New Future", player
    )

    for i in range (world.options.starting_shard,world.options.shard_goal + 1 if world.options.remove_post_victory_locations else 15):
        if i > 10:
            set_rule_if_exists(
                f"Disaster Shard {i-10} Boss", lambda state, val=i: state.has("Progressive Shard", player, val-1)
            )
        else:
            set_rule_if_exists(
                f"Shard {i} Boss", lambda state, val=i: state.has("Progressive Shard", player, val-1)
            )

    if world.options.shopsanity == 1:
        # per-shard
        for i in range(world.options.starting_shard,world.options.shard_goal + 1 if world.options.remove_post_victory_locations else 15):
            limit = world.options.pershard_shopsanity_quantity if world.options.pershard_shopsanity_scaling == 1 else int(((world.options.pershard_shopsanity_dynamic_quantity)/100)*(SHARD_LENGTHS[i-1]//2))
            for j in range(1, limit+1):
                if i > 10:
                    set_rule_if_exists(
                        f"Disaster Shard {i-10} Shop Item {j:02}", lambda state: (True)
                    )
                else:
                    set_rule_if_exists(
                        f"Shard {i} Shop Item {j:02}", lambda state: (True)
                    )
    elif world.options.shopsanity == 2:
        # global
        for j in range(1, world.options.global_shopsanity_quantity+1):
            set_rule_if_exists(
                f"Global Shop Item {j:03}", lambda state: (True)
            )
            # add_item_rule for shops to not contain local items if the setting is enabled
            # add_item_rule(location, lambda item: not (item.player == player and item.name in ["Cranky", "Funky", "Candy", "Snide"]))

    if world.options.fragmentsanity == 1:
        # per-shard fragment clears
        for i in range(world.options.starting_shard,world.options.shard_goal + 1 if world.options.remove_post_victory_locations else 15):
            limit = world.options.pershard_fragmentsanity_quantity if world.options.pershard_fragmentsanity_scaling == 1 else int(((world.options.pershard_fragmentsanity_dynamic_quantity)/100)*SHARD_LENGTHS[i-1])
            for j in range(1, limit+1):
                if i > 10:
                    set_rule_if_exists(
                        f"Disaster Shard {i-10} Fragment Clear {j:02}", lambda state: (True)
                    )
                else:
                    set_rule_if_exists(
                        f"Shard {i} Fragment Clear {j:02}", lambda state: (True)
                    )
    elif world.options.fragmentsanity == 2:
        # global fragment clears
        for j in range(1, world.options.global_fragmentsanity_quantity+1):
            set_rule_if_exists(
                f"Global Fragment Clear {j:02}", lambda state: (True)
            )

    if world.options.captains_upgrades == 1:
        # i feel like this could be simplified but idc
        for i in range(1, 5):
            set_rule_if_exists(f"Captain's Max Health Upgrade Purchase {i}", lambda state, vali=i : has_purchasable_shards(state, vali) and has_NPC(state, "The Captain"))
        set_rule_if_exists("Captain's Max Lives Upgrade Purchase", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "The Captain"))
        for i in range(1, 5):
            set_rule_if_exists(f"Captain's Max Energy Upgrade Purchase {i}", lambda state, vali=i : has_purchasable_shards(state, vali) and has_NPC(state, "The Captain"))
        for i in range(1, 7):
            set_rule_if_exists(f"Captain's Item Rarity Upgrade Purchase {i}", lambda state, vali=i : has_purchasable_shards(state, vali) and has_NPC(state, "The Captain"))
        for i in range(1, 4):
            set_rule_if_exists(f"Captain's Sparks in Fragments Upgrade Purchase {i}", lambda state, vali=i : has_purchasable_shards(state, vali) and has_NPC(state, "The Captain"))
        for i in range(1, 4):
            set_rule_if_exists(f"Captain's Starting Sparks Upgrade Purchase {i}", lambda state, vali=i : has_purchasable_shards(state, vali) and has_NPC(state, "The Captain"))

    if world.options.weeboh_purchases >= 1:
        # i feel like this could be simplified but idc
        if world.options.weeboh_purchases >= 2:
            # Green/Blue are unobtainable in the scope of AP with vanilla fashion unlocks
            set_rule_if_exists("Costume Purchase: Little Sister", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh"))
            set_rule_if_exists("Costume Purchase: Supersonic Zoe", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh"))
        set_rule_if_exists("Costume Purchase: Zoe the Shadow", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh"))
        set_rule_if_exists("Costume Purchase: Zoe 64", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh"))
        set_rule_if_exists("Costume Purchase: Totally Accurate Zoe", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh") and fashion_unlock(state, 5))
        if not world.options.remove_post_victory_locations or world.options.shard_goal >= 7 or world.options.weeboh_purchases == 3: set_rule_if_exists("Costume Purchase: Flopsy", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh") and fashion_unlock(state, 6))
        if not world.options.remove_post_victory_locations or world.options.shard_goal >= 5 or world.options.weeboh_purchases == 3: set_rule_if_exists("Costume Purchase: Weeboh", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh") and fashion_unlock(state, 10))
        if not world.options.remove_post_victory_locations or world.options.shard_goal >= 11 or world.options.weeboh_purchases == 3: set_rule_if_exists("Costume Purchase: Crispy", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh") and fashion_unlock(state, 1))
        if not world.options.remove_post_victory_locations or world.options.shard_goal >= 12 or world.options.weeboh_purchases == 3: set_rule_if_exists("Costume Purchase: Twisted Flopsy", lambda state : has_purchasable_shards(state, 1) and has_NPC(state, "Fashion Weeboh") and fashion_unlock(state, 7))


    set_rule_if_exists(
        "Wraith's Hourglass Purchase", lambda state: has_purchasable_shards(state, 1) and has_NPC(state, "Wraith")
    )
    set_rule_if_exists(
        "Heir's Javelin Purchase", lambda state: has_purchasable_shards(state, 1) and has_NPC(state, "Niada")
    )
    set_rule_if_exists(
        "Sage's Cowl Purchase", lambda state: has_purchasable_shards(state, 1) and has_NPC(state, "Daro")
    )
