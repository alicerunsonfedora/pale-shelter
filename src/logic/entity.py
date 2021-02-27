#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from math import sqrt
from random import randint
from typing import Tuple
from src.logic.player import Player


class NonPlayerEntity():
    """A non-player entity that a player can interact with to attempt to get into a relationship with."""

    def __init__(self, name: str, position: Tuple[int, int]) -> None:
        """Create an entity.

        Arguments:
            position (tuple): The entity's position on the map.
        """
        self.image_name = name.lower()
        self.position = position
        self.max_love_level = float(randint(1, 10))
        self.current_love_level = 0.0
        self.love_seed = bool(randint(0, 1))

    @property
    def fulfilled(self):
        return self.current_love_level == self.max_love_level

    def is_near(self, player: Player) -> bool:
        """Returns whether the entity is near a player in the world."""
        ex, ey = self.position
        px, py = player.position

        distance = sqrt(pow(px - ex, 2) + pow(py - ey, 2))
        return distance < 48

    def transfer(self, amount: float):
        """Transfers the love amount from one source to another."""
        self.current_love_level += amount
        if self.current_love_level >= self.max_love_level:
            self.current_love_level = self.max_love_level

    def verify(self) -> bool:
        """Returns whether the entity accepts/rejects the relationship."""
        return self.fulfilled and self.love_seed
