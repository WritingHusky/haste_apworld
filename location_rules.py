from typing import Callable
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from .Locations import LOCATION_TABLE


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

    player = world.player

    world.multiworld.completion_condition[player] = lambda state: state.has(
        "A New Future", player
    )

    set_rule_if_exists("Shard 1 Boss", lambda state: (True))

    for i in range (2,world.options.shard_goal + 1 if world.options.remove_post_victory_locations else 11):
        set_rule_if_exists(
            f"Shard {i} Boss", lambda state, val=i: state.has("Progressive Shard", player, val-1)
        )

    if world.options.shopsanity == 1:
        # per-shard;
        for i in range(1,world.options.shard_goal + 1 if world.options.remove_post_victory_locations else 11):
            for j in range(1, world.options.shopsanity_quantity+1):
                set_rule_if_exists(
                    f"Shard {i} Shop Item {j}", lambda state: (True)
                )
    elif world.options.shopsanity == 2:
        # global
        for j in range(1, world.options.shopsanity_quantity+1):
            set_rule_if_exists(
                f"Global Shop Item {j}", lambda state: (True)
            )
            # add_item_rule for shops to not contain local items if the setting is enabled
            # add_item_rule(location, lambda item: not (item.player == player and item.name in ["Cranky", "Funky", "Candy", "Snide"]))

    if world.options.fragmentsanity >= 1:
        # fragment clears
        for j in range(1, world.options.fragmentsanity_quantity+1):
            set_rule_if_exists(
                f"Fragment Clear {j}", lambda state: (True)
            )


    set_rule_if_exists(
        "Ability Slomo", lambda state: state.has("Progressive Shard", player, 1) and has_NPC(state, "Wraith")
    )
    set_rule_if_exists(
        "Ability Grapple", lambda state: state.has("Progressive Shard", player, 1) and has_NPC(state, "Niada")
    )
    set_rule_if_exists(
        "Ability Fly", lambda state: state.has("Progressive Shard", player, 1) and has_NPC(state, "Daro")
    )
