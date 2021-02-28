#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import Tuple, Callable
from pygame import Rect
from src.logic.player import Player


class Powerup():
    """A class representing an in-game powerup."""

    def __init__(self, position: Tuple[int, int], texture_tile: Tuple[int, int], on_activate: Callable) -> None:
        """Create a powerup in the game.

        Arguments:
            position (tuple): The position of the powerup on the screen or surface.
            texture_tile (tuple): The tileset position in the powerups tilesheet to render.
            on_activate (callable): The method to run when the powerup is collected.
        """
        self.canvas_position = left, top = position
        self.texture_position = texture_tile
        self.callback = on_activate
        self.activated = False
        self.boundaries = Rect(left, top, 48, 48)
        self.kind = "empty"

    def activate_event(self, player: Player):
        """Activate the powerup if the player has collided with it and the powerup hasn't been used already."""
        if not self.boundaries.collidepoint(player.position) or self.activated:
            return
        self.callback()
        self.activated = True
