#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The player module contains code surrounding the player in the game."""
import pygame
from random import random
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
        self.love_meter = 100.0

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

    def read_from_pressed(self, pressed: Dict[int, bool]) -> float:
        """Update the position of the player based on what keys are being pressed, and change the love accordingly."""
        self.position = self.calculate_position(pressed)
        transfer = 0.0

        if pressed[pygame.K_e]:
            transfer = 0.5
            self.subtract_love(0.5)

        return transfer

    def update_love(self) -> None:
        """Randomly drain the love on every tick."""
        if self.love_meter <= 0.0:
            self.love_meter = 0.0
        else:
            self.love_meter -= random() * 0.00001

    def add_love(self, amount: float) -> None:
        """Add love by a given amount."""
        self.love_meter += amount
        if self.love_meter >= 100.0:
            self.love_meter = 100.0

    def subtract_love(self, amount: float) -> None:
        """Subtract love by a given amount."""
        if self.love_meter <= 0.0:
            self.love_meter = 0.0
        else:
            self.love_meter -= amount
