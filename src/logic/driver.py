#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from os import path
from typing import List, Tuple
from src.logic.player import Player
from src.logic.entity import NonPlayerEntity
from src.data.levels import Level
import pygame
from src.assets import Tilesheet, ColorPalette, asset_path


class PaleShelter():
    """The main application class for the game."""

    def __init__(self, window_size: Tuple[int, int] = (1280, 720), fps: int = 60) -> None:
        """Set up the game's canvas, colors, tilesheets, and event listeners."""

        self.canvas = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        pygame.display.set_caption("No Love")

        self.frame_limiter = pygame.time.Clock()
        self.fps = fps

        self.palette = ColorPalette(asset_path(
            "assets/palettes/nostalgia36.gpl"))
        self.palette.assign_color_name("DARK_BLACK", "1e2029")

        self.ts_structures = Tilesheet(
            asset_path("assets/tilesets/struct01.png"), (48, 48), (12, 16))

        self.player = Player((200, 200), 4)
        self.level = Level(asset_path("data/random01.lvl"))

        self.entities: List[NonPlayerEntity] = []
        self.game_over = False

    def manage_game_events(self) -> bool:
        """Manage the primary game events such as quitting, player movement, etc."""
        self.frame_limiter.tick(self.fps)

        self.player.update_love()
        if self.player.love_meter <= 0:
            print("Player is out of love!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        pressed = pygame.key.get_pressed()
        transfer = self.player.read_from_pressed(pressed)

        if transfer:
            for entity in self.entities:
                if not entity.is_near(self.player):
                    continue
                entity.transfer(transfer)
                if entity.verify():
                    self.game_over = True

        return True

    def update_canvas(self) -> None:
        """Update the contents of the canvas."""

        # Fill the canvas with a black-like color.
        self.canvas.fill(self.palette.get_color("DARK_BLACK"))

        # Get the width and the height of the level, tiles, and the window.
        l_width, l_height = self.level.dimensions
        t_width, t_height = self.ts_structures.tile_size
        c_width, c_height = pygame.display.get_window_size()

        # Get the center of the screen.
        center_x, center_y = c_width / 2, c_height / 2

        # Determine the offsets at which to draw the first tile on the screen.
        offset_x = center_x - (t_width * (l_width / 2))
        offset_y = center_y - (t_height * (l_height / 2))

        # Create a coordinate that will represent the tiles, starting with the first tile from the offset.
        tile_x, tile_y = offset_x, offset_y

        # Iterate through all of the tilemap rows, filling the tilemap slowly.
        for row in self.level.tiles:

            # Fill in the tile with the appropriate tileset image at that position, or don't fill anything if the tile
            # is an "air" tile.
            for cx, cy in row:
                if cx != -1 and cy != -1:
                    self.canvas.blit(
                        self.ts_structures.get_tile(cx, cy), (tile_x, tile_y))
                tile_x += t_width

            # Move to the next row and reset the X position.
            tile_y += t_height
            tile_x = offset_x

    def render(self) -> None:
        """Render the changes onto the screen."""
        pygame.display.update()
