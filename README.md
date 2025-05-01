# Haste

## Installation & Usage

See the [setup guide](https://github.com/WritingHusky/haste_apworld/blob/main/docs/setup_en.md) for instructions.

## What does randomization do to this game?

Shards are locked behind an unlock item. Abilites are shuffled into the item pool. Buy an item at a shop and beat the boss per shard to check an item into the ap world.

## What are the Items in this ApWorld?

- Progressive Shard: Unlocks the next shard
- Ability (Slomo, Grapple, Fly): Give the player that ability.
- Anti-Spark Bundle: Give you an amount of anti-sparks

## What location are in the ApWorld?

- Shard x Boss: Defeating the boss in shard x.
- Shard x Shop Item: Buy any item in a shop in shard x. (1 per shard)
- Ability Slomo, Grapple, Fly: Getting the ability from the respective character in the hub.

## What is the goal of Haste?

The goal of Haste is to beat the end boss of the final shard.

## When the player receives an item, what happens?

The item will imdeitaly come into affect. If force reload is enabled and you are in the hub, getting a progressive shard will reload the hub to unlock the next shard.

## I need help! What do I do?

Refer to the troubleshooting steps in the [setup guide](https://github.com/WritingHusky/haste_apworld/blob/main/docs/setup_en.md)/ Then, if you are still stuck, please ask in the Haste thread (under `future-game-design`) in the Archipelago server.

## State of the rando

See [state of the world](https://github.com/WritingHusky/haste_apworld/blob/main/docs/CurrentState.md) for more information about the current state (as i understand it) about this randomizer.

## Running from source

### Installing Git

Download and install git from here: https://git-scm.com/downloads  
Then clone this repository with git by running this in a command prompt:

```
git clone https://github.com/WritingHusky/haste_apworld.git
```

### Installing Python

You will need to install Python 3.12. We recommend using `pyenv` to manage different Python versions:

- For Windows, install `pyenv-win` by following
  [these steps](https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#quick-start).
- For Linux, follow the instructions [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#automatic-installer) to
  install `pyenv` and then follow the instructions
  [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv) to set up your shell
  environment.

After installing `pyenv`, install and switch to Python 3.12 by running:

```sh
pyenv install 3.12
pyenv global 3.12
```

## Credits

This randomizer would not be possible without the help from:

- Landfall games: for making the game with modding in mind
- People in the Haste Discord mod-developer-chat: for helping me learn to mod games
