#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import Dict, Tuple


class ColorPalette():
    """A class that handles color palettes for different colors in a file.

    The color palette accepts paths to GIMP Palette (GPL) files and will store them in a dictionary. A name registry
        is also available to get a color based off of a given name.
    """

    def __init__(self, filepath: str):
        """Initialize a color palette from a file.

        Arguments:
            filepath (str): The path to the color palette file to get the colors for.
        """
        self.colors = parse_gpl_file(filepath)
        self.names = {}

    def assign_color_name(self, name: str, color: str):
        """Assigns a name to a given hexadecimal color."""
        if color not in self.colors:
            raise KeyError(f"{color} doesn't exist in this palette.")
        if name in self.names:
            raise KeyError(f"{name} cannot be assigned to multiple colors.")
        self.names[name] = color

    def get_color(self, name: str) -> Tuple[int, int, int]:
        """Returns the color associated with a specified name, or black if the name can't be found."""
        return self.colors.get(self.names[name], (0, 0, 0))


def parse_gpl_file(filepath: str) -> Dict[str, Tuple[int, int, int]]:
    """Parse a GIMP Palette file (GPL) into a dictionary.

    Arguments:
        filepath (str): The path to the palette file to parse.

    Returns:
        A dictionary with hex colors as keys and the RGB tuple as values.
    """
    palette = {}

    with open(filepath, 'r', encoding="utf-8") as file_object:
        file_lines = [line for line in file_object.readlines()
                      if not line.startswith("#")]

    if file_lines[0] != "GIMP Palette\n":
        raise TypeError(f"{filepath} is not a valid GPL file.")
    file_lines.pop(0)

    for line in file_lines:
        data = line.strip().split("\t")
        if len(data) != 4:
            raise TypeError(f"{filepath} appears to be malformed.")

        color_key = data.pop()
        rgb_values = tuple([int(val) for val in data])

        palette[color_key] = rgb_values

    return palette
