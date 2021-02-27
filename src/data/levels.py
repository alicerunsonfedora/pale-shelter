#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import List, Tuple, Dict, NewType
from src.data.tileset_defs import parse_tiles


class Level():
    """A class that includes data about a level from a level file.

    Class Attributes:
        src (str): The path to the file that generated this level.
        tileset_name (str): The tileset being used in this level.
        dimensions (tuple): A tuple containing the size of the level.
        tile_definitions (dict): A dictionary with characters as keys and a position in the tileset as their values.
            This dictionary defines what tile is used in place of an ASCII character in the level file.
        tiles (list): A two-dimensional array containing the tileset positions to be drawn to the screen.
    """

    def __init__(self, filepath):
        """Creates a level from a file.

        Arguments:
            filepath(str): The path to the file to open and parse level data from.
        """
        self.src = filepath

        self.tileset_name: str = ""
        self.decor_tileset_name: str = ""

        self.dimensions: Tuple[int, int] = (0, 0)

        self.tile_definitions: Dict[str, Tuple[int, int]] = {" ": (-1, -1)}
        self.tiles: List[List[Tuple[int, int]]] = []

        self.entities: List[Tuple[str, Tuple[int, int]]] = []

        self.decor_definitions: Dict[str, Tuple[int, int]] = {" ": (-1, -1)}
        self.decor: List[List[Tuple[int, int]]] = []

        self.collidable_tiles: List[Tuple[int, int]] = []

        self.powerups: List[Tuple[int, int]] = []

        with open(filepath, "r") as file:
            self._parse_file([lin.strip("\n") for lin in file.readlines(
            ) if lin != "\n" and not lin.startswith("#")])

    def __str__(self):
        return f"Level(tileset={self.tileset_name}, size={self.dimensions}, definitions={self.tile_definitions})"

    def is_collidable(self, coordinate: Tuple[int, int]) -> bool:
        x, y = coordinate
        return self.tiles[x][y] in self.collidable_tiles

    def _parse_file(self, source: List[str]):
        if source[0] != "LIFELIGHT LEVEL":
            raise TypeError("File header for level file is corrupt.")
        source.pop(0)

        tileset_name = source.pop(0).split(" ")
        if tileset_name[0] != "TILESET":
            raise TypeError("Tileset data is missing or corrupt.")
        self.tileset_name = tileset_name[1].lower().strip()

        decor_name = source.pop(0).split(" ")
        if decor_name[0] != "DECOR":
            source.insert(0, " ".join(decor_name))
        else:
            self.decor_tileset_name = decor_name[1].lower().strip()

        dimensions = source.pop(0).split("  ")
        if dimensions[0] != "SIZE":
            raise TypeError("Level dimensions is missing or corrupt.")
        self.dimensions = tuple([int(dim) for dim in dimensions[1:]])

        if self.tileset_name.startswith("#"):
            _, self.tile_definitions, collidable_tile_data = parse_tiles(
                f"data/ts_defs/{self.tileset_name[1:]}.tsd")

            for tile in self.tile_definitions:
                if collidable_tile_data[tile]:
                    self.collidable_tiles.append(self.tile_definitions[tile])

        else:
            if source.pop(0) != "BEGIN DEFINITIONS":
                raise TypeError("Definition block is missing or corrupt.")

            while (data := source.pop(0)) != "END DEFINITIONS":
                properties = data.split("  ")
                self.tile_definitions[properties[0]] = tuple(
                    [int(val) for val in properties[1:]])

        if self.decor_tileset_name.startswith("#"):
            self.decor_definitions = parse_tiles(
                f"data/ts_defs/{self.decor_tileset_name[1:]}.tsd")[1]
        else:
            if source.pop(0) == "BEGIN DECOR DEFINITIONS":
                while (data := source.pop(0)) != "END DECOR DEFINITIONS":
                    properties = data.split("  ")
                    self.decor_definitions[properties[0]] = tuple(
                        [int(val) for val in properties[1:]])

        if source.pop(0) != "BEGIN LAYOUT":
            raise TypeError("Layout block is missing or corrupt.")

        while (data := source.pop(0)) != "END LAYOUT":
            self.tiles.append([self.tile_definitions[tile] for tile in data])

        if source.pop(0) == "BEGIN DECOR LAYOUT":
            while (data := source.pop(0)) != "END DECOR LAYOUT":
                self.decor.append([self.decor_definitions[tile]
                                   for tile in data])

        if source.pop(0) != "BEGIN ENTITIES":
            raise TypeError("Entity block is missing or corrupt.")

        while (data := source.pop(0)) != "END ENTITIES":
            entity_data = data.split("  ")
            self.entities.append((entity_data[0], tuple(
                [int(val) for val in entity_data[1:]])))

        if source.pop(0) == "BEGIN POWERUPS":
            while (data := source.pop(0)) != "END POWERUPS":
                self.powerups.append(
                    tuple([int(val) for val in data.split("  ")]))
