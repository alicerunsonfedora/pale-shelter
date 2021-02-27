#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The player module contains code surrounding the player in the game."""
import pygame
from random import random
from typing import List, Tuple, Dict


class Player():
    """A class that represents the main player."""

    def __init__(self, origin: Tuple[int, int] = (0, 0), speed: int = 1) -> None:
        """Create a player with an origin an speed.

        Arguments:
            origin (tuple): The position of the player when the level starts. Defaults to the origin (0, 0).
            speed (int): The rate at which the player moves on screen. Defaults to 1.
        """
        self.position = left, top = origin
        self.move_rate = speed
        self.love_meter = 100.0
        self.bounds = pygame.Rect(left, top, 36, 36)
        self.current_interval = 0.0
        self.image_name = "amelia"

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

    def update_position(self, pressed: Dict[int, bool], delta_time: float, collidable_tiles: List[pygame.Rect] = []) -> None:
        """Update the position of the player based on what keys are being pressed, and change the love accordingly."""
        new_position = left, top = self.calculate_position(pressed)
        if new_position == self.position:
            return

        colliding = False
        new_player_bounds = pygame.Rect(left, top, 36, 36)
        for tile in collidable_tiles:
            if bool(tile.colliderect(new_player_bounds)):
                colliding = True
        if colliding:
            return

        self.position = new_position
        self.current_interval += delta_time
        # TODO: Write code here to switch frames.

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
