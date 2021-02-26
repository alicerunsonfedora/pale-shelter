#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import Dict, Tuple
from src.assets import asset_path


def parse_tiles(filepath: str) -> Tuple[str, Dict[str, Tuple[int, int]]]:
    """Parse a tileset definition file and get the definitions for a given tileset.

    Arguments:
        filepath (str): The relative path to the tileset definition file to parse.

    Returns:
        A tuple containing the tileset name and a dictionary of definitions for the tiles.
    """
    definitions = {' ': (-1, -1)}
    with open(asset_path(filepath), "r") as file:
        source = [line.strip() for line in file.readlines()
                  if line != "\n" and not line.startswith("#")]

    if source.pop(0) != "LIFELIGHT TILESET":
        raise TypeError("Tileset definition header is missing or corrupt.")

    tileset_name_schema = source.pop(0).split(" ")
    if tileset_name_schema[0] != "TILESET" or len(tileset_name_schema) != 2:
        raise TypeError("Tileset name has not been defined.")
    ts_name = tileset_name_schema[1]

    if source.pop(0) != "BEGIN DEFINITIONS":
        raise TypeError("Expected beginning of definition block.")

    while (data := source.pop(0)) != "END DEFINITIONS":
        definition_line = data.split("  ")
        definitions[definition_line[0]] = tuple(
            [int(i) for i in definition_line[1:]])

    return ts_name, definitions
