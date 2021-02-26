#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""This module contains classes to handle tilesheets in PyGame."""

from typing import Tuple
import pygame


class Tile():
    """A data class that represents a tile in a tilesheet."""

    def __init__(self, x, y, size):
        self.x: int = x
        self.y: int = y
        self.width, self.height = size

    @property
    def size(self) -> Tuple[int, int]:
        """Returns the size of the tile."""
        return self.width, self.height

    @property
    def position(self) -> Tuple[int, int]:
        """Returns the position of the tile in a tilesheet."""
        return self.x, self.y

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Tile) and self.position == o.position and self.size == o.size

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"Tile(position={self.position}, size={self.size})"


class Tilesheet():
    """A class that handles splitting tile sheets into a tile set for use in PyGame."""

    def __init__(self, path: str, image_size: Tuple[int, int], sheet_size: Tuple[int, int]) -> None:
        """Creates a tile sheet.

        Arguments:
            path (str): The filepath to the image to load the tilesheet from.
            image_size (int, int): The size of the tiles in the tilesheet.
            sheet_size (int, int): The dimensions of the tiles in the tilesheet.
        """
        self._rows, self._cols = sheet_size
        self._width, self._height = image_size
        self._image = pygame.image.load(path).convert()
        self._lut = [[Tile(x * self._width, y * self._width, (self._width, self._height))
                      for y in range(0, self._rows)] for x in range(0, self._cols)]
        self._registry = {}

    @property
    def tile_size(self) -> Tuple[int, int]:
        """Returns the size of a given tile in the tilesheet."""
        return self._width, self._height

    def get_tile(self, x: int, y: int) -> pygame.Surface:
        """Returns the tile specified at a given position in the tilesheet.

        Arguments:
            x (int): The x position of the tile.
            y (int): The y position of the tile.

        Returns:
            The image subsurface at the specified position in the tilesheet.
        """
        _tile = self._lut[x][y]
        return self._image.subsurface((_tile.x, _tile.y, _tile.width, _tile.height))

    def get_named_tile(self, name: str, fallback_position: Tuple[int, int] = (0, 0)) -> pygame.Surface:
        """Returns a tile with a specified name.

        Arguments:
            name (str): The name of the tile in the tilesheet registry to fetch.
            fallback_position (tuple): THe X and Y coordinates to use if the name lookup fails.

        Returns:
            The image subsurface of the corresponding tile.
        """
        if name not in self._registry:
            x, y = fallback_position
            return self.get_tile(x, y)
        return self._registry[name]

    def register_tile_name(self, name: str, position: Tuple[int, int]):
        """Associate a tile with a name for easy lookup.

        Arguments:
            name (str): The name to associate with a tile.
            position (tuple): The position of the tile in the tilesheet.
        """
        x, y = position
        if name in self._registry:
            return
        self._registry[name] = self.get_tile(x, y)
