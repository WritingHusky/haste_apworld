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



    # TODO: once i figure out regions, make the shops unlock in chunks of 5 (so everything isnt considered sphere 0)
    # also regions will probably fix the Stupid Python Bug where non-Shard1 shops only become in-logic once all shards are collected
    if world.options.shopsanity == 1:
        # pershard;
        for i in range(1,11):
            for j in range(1, world.options.shopsanity_quantity+1):
                if i == 1:
                    set_rule_if_exists(
                        f"Shard {i} Shop Item {j}", lambda state: (True)
                    )
                else:
                    set_rule_if_exists(
                        f"Shard {i} Shop Item {j}", lambda state: state.has("Progressive Shard", player, i-1)
                    )

    elif world.options.shopsanity == 2:
        # global
        for j in range(1, world.options.shopsanity_quantity+1):
            set_rule_if_exists(
                f"Global Shop Item {j}", lambda state: (True)
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
