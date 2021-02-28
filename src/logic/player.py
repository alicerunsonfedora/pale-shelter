#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The player module contains code surrounding the player in the game."""
from src.assets.pyinst import asset_path
import pygame
from random import random
from typing import List, Tuple, Dict
from src.assets import Tilesheet


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
        self.bounds = pygame.Rect(left, top, 48, 48)
        self.current_interval = 0.0
        self.current_frame = 0
        self.image_name = "amelia"
        self.facing = "south"
        self.in_motion = False
        self.idle_tilesheet = Tilesheet(asset_path(
            f"assets/characters/{self.image_name}_idle.png"), (48, 96), (1, 4))
        self.run_tilesheet = Tilesheet(asset_path(
            f"assets/characters/{self.image_name}_run.png"), (48, 96), (1, 24))

        self.directions = {
            "east": 0,
            "north": 1,
            "west": 2,
            "south": 3
        }

    def get_texture(self):
        """Returns the appropriate texture for the player in the game loop."""
        if not self.in_motion:
            return self.idle_tilesheet.get_tile(self.directions[self.facing], 0)
        else:
            endpoints = {"east": 0, "north": 6, "west": 12, "south": 18}
            row = self.current_frame + endpoints[self.facing]
            return self.run_tilesheet.get_tile(row, 0)

    def calculate_position(self, pressed: Dict[int, bool]) -> Tuple[int, int]:
        """Returns the new position based on what keys are pressed."""
        x, y = self.position
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            x -= self.move_rate
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            x += self.move_rate
        if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            y -= self.move_rate
        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            y += self.move_rate
        return x, y

    def update_position(self, pressed: Dict[int, bool], delta_time: float, collidable_tiles: List[pygame.Rect] = []) -> None:
        """Update the position of the player based on what keys are being pressed, and change the love accordingly."""
        self.current_interval += delta_time
        if self.current_interval > delta_time * 2:
            self.current_interval = 0

        if self.current_interval == delta_time * 2:
            self.current_frame += 1
            if self.current_frame >= 6:
                self.current_frame = 0

        new_position = left, top = self.calculate_position(pressed)
        if new_position == self.position:
            self.in_motion = False
            self.current_frame = 0
            return

        colliding = False
        new_player_bounds = pygame.Rect(left, top, 36, 36)
        for tile in collidable_tiles:
            if bool(tile.colliderect(new_player_bounds)):
                colliding = True
        if colliding:
            return

        self.in_motion = True
        x, y = self.position
        delta_x, delta_y = left - x, top - y

        if delta_x > delta_y and delta_x > 0:
            self.facing = "east"
        elif delta_y > delta_x and delta_y > 0:
            self.facing = "south"
        elif delta_x < delta_y and delta_x < 0:
            self.facing = "west"
        elif delta_y < delta_x and delta_y < 0:
            self.facing = "north"

        self.position = new_position

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
