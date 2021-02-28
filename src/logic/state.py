#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The state module contains the utilities used to maintain game states across playthroughs."""

from enum import Enum


class GameState(Enum):
    """An enumeration for the different game states available."""
    MENU = "menu"
    IN_GAME = "in_game"
    GAME_OVER = "game_over"
    EXIT = "exit"


class GameStateManager():
    """A basic class for handling multiple states.

    Class Attributes:
        state (GameState): The current game state.
        player_meter (float): The player's current love meter status ("health")
    """

    def __init__(self):
        self.state = GameState.MENU
        self.player_meter = 100.0
