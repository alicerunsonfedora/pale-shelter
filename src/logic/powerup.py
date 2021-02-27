#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import Tuple, Callable
from pygame import Rect
from src.logic.player import Player


class Powerup():
    def __init__(self, position: Tuple[int, int], texture_tile: Tuple[int, int], on_activate: Callable):
        self.canvas_position = left, top = position
        self.texture_position = texture_tile
        self.callback = on_activate
        self.activated = False
        self.boundaries = Rect(left, top, 48, 48)

    def activate_event(self, player: Player):
        if not self.boundaries.collidepoint(player.position) or self.activated:
            return
        self.callback()
        self.activated = True
