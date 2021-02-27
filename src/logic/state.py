#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
from enum import Enum


class GameState(Enum):
    MENU = "menu"
    IN_GAME = "in_game"
    GAME_OVER = "game_over"
    EXIT = "exit"


class GameStateManager():
    def __init__(self):
        self.state = GameState.MENU
