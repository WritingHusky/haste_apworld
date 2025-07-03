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

    for i in range (2,11):
        set_rule_if_exists(
            f"Shard {i} Boss", lambda state, val=i: state.has("Progressive Shard", player, val-1)
        )


    # TODO: once i figure out regions, make the shops unlock in chunks of 5 (so everything isnt considered sphere 0)
    if world.options.shopsanity == 1:
        # pershard;
        for i in range(1,11):
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

    set_rule_if_exists(
        "Ability Slomo", lambda state: state.has("Progressive Shard", player, 1)
    )
    set_rule_if_exists(
        "Ability Grapple", lambda state: state.has("Progressive Shard", player, 1)
    )
    set_rule_if_exists(
        "Ability Fly", lambda state: state.has("Progressive Shard", player, 1)
    )
