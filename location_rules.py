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

    player = world.player

    world.multiworld.completion_condition[player] = lambda state: state.has(
        "Victory", player
    )

    set_rule_if_exists("Shard 1 Boss", lambda state: (True))
    set_rule_if_exists(
        "Shard 2 Boss", lambda state: state.has("Progressive Shard", player, 1)
    )
    set_rule_if_exists(
        "Shard 3 Boss", lambda state: state.has("Progressive Shard", player, 2)
    )
    set_rule_if_exists(
        "Shard 4 Boss", lambda state: state.has("Progressive Shard", player, 3)
    )
    set_rule_if_exists(
        "Shard 5 Boss", lambda state: state.has("Progressive Shard", player, 4)
    )
    set_rule_if_exists(
        "Shard 6 Boss", lambda state: state.has("Progressive Shard", player, 5)
    )
    set_rule_if_exists(
        "Shard 7 Boss", lambda state: state.has("Progressive Shard", player, 6)
    )
    set_rule_if_exists(
        "Shard 8 Boss", lambda state: state.has("Progressive Shard", player, 7)
    )
    set_rule_if_exists(
        "Shard 9 Boss", lambda state: state.has("Progressive Shard", player, 8)
    )
    set_rule_if_exists(
        "Shard 10 Boss", lambda state: state.has("Progressive Shard", player, 9)
    )
    set_rule_if_exists("Shard 1 Shop Item", lambda state: (True))
    set_rule_if_exists(
        "Shard 2 Shop Item", lambda state: state.has("Progressive Shard", player, 1)
    )
    set_rule_if_exists(
        "Shard 3 Shop Item", lambda state: state.has("Progressive Shard", player, 2)
    )
    set_rule_if_exists(
        "Shard 4 Shop Item", lambda state: state.has("Progressive Shard", player, 3)
    )
    set_rule_if_exists(
        "Shard 5 Shop Item", lambda state: state.has("Progressive Shard", player, 4)
    )
    set_rule_if_exists(
        "Shard 6 Shop Item", lambda state: state.has("Progressive Shard", player, 5)
    )
    set_rule_if_exists(
        "Shard 7 Shop Item", lambda state: state.has("Progressive Shard", player, 6)
    )
    set_rule_if_exists(
        "Shard 8 Shop Item", lambda state: state.has("Progressive Shard", player, 7)
    )
    set_rule_if_exists(
        "Shard 9 Shop Item", lambda state: state.has("Progressive Shard", player, 8)
    )
    set_rule_if_exists(
        "Shard 10 Shop Item", lambda state: state.has("Progressive Shard", player, 9)
    )
    set_rule_if_exists(
        "Ability Slomo", lambda state: state.has("Progressive Shard", player, 1)
    )
    set_rule_if_exists(
        "Ability Grapple", lambda state: state.has("Progressive Shard", player, 1)
    )
    set_rule_if_exists(
        "Ability Fly", lambda state: state.has("Progressive Shard", player, 1)
    )
