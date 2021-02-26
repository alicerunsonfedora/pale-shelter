#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The player module contains code surrounding the player in the game."""
import pygame
from typing import Tuple, Dict


class Player():
    """A class that represents the main player."""

    def __init__(self, origin: Tuple[int, int] = (0, 0), speed: int = 1) -> None:
        """Create a player with an origin an speed.

        Arguments:
            origin (tuple): The position of the player when the level starts. Defaults to the origin (0, 0).
            speed (int): The rate at which the player moves on screen. Defaults to 1.
        """
        self.position = origin
        self.move_rate = speed

    def calculate_position(self, pressed: Dict[int, bool]) -> Tuple[int, int]:
        """Returns the new position based on what keys are pressed."""
        x, y = self.position
        if pressed[pygame.K_a]:
            x -= self.move_rate
        if pressed[pygame.K_d]:
            x += self.move_rate
        if pressed[pygame.K_w]:
            y -= self.move_rate
        if pressed[pygame.K_s]:
            y += self.move_rate
        return x, y

    def update_position(self, pressed: Dict[int, bool]):
        """Update the position of the player based on what keys are being pressed."""
        self.position = self.calculate_position(pressed)
