#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import Dict, List, Tuple
from src.logic.player import Player
from src.logic.entity import NonPlayerEntity
from src.logic.powerup import Powerup
from src.data.levels import Level
import pygame
from src.assets import Tilesheet, ColorPalette, asset_path


class PaleShelter():
    """The main application class for the game."""

    def __init__(self, window_size: Tuple[int, int] = (1280, 720), fps: int = 60) -> None:
        """Set up the game's canvas, colors, tilesheets, and event listeners."""

        self.canvas = pygame.display.set_mode(window_size)
        pygame.display.set_caption("No Love")

        self.frame_limiter = pygame.time.Clock()
        self.fps = fps

        self.palette = ColorPalette(asset_path(
            "assets/palettes/nostalgia36.gpl"))
        self.palette.assign_color_name("DARK_BLACK", "1e2029")
        self.palette.assign_color_name("PINK", "ff9e95")

        self.ts_structures = Tilesheet(
            asset_path("assets/tilesets/struct01.png"), (48, 48), (9, 9))
        self.ts_decor = Tilesheet(asset_path(
            "assets/tilesets/decor01.png"), (48, 48), (22, 24))

        self.level = Level(asset_path("data/random01.lvl"))
        self.player = Player(self._init_entity_position("PLAYER"), 4)

        self.collidables = []
        self.made_first_paint = False

        self.entities: List[NonPlayerEntity] = []
        self.game_over = False

        for name, _ in self.level.entities:
            if name == "PLAYER":
                continue
            self.entities.append(NonPlayerEntity(
                self._init_entity_position(name)))

        self.powerups: List[Powerup] = []
        for powerup in self.level.powerups:
            self.powerups.append(self._init_powerup(powerup))

    def _init_entity_position(self, entity) -> Tuple[int, int]:
        position = 0, 0
        for ent_name, ent_position in self.level.entities:
            if ent_name != entity:
                continue
            position = ent_position
            break

        l_width, l_height = self.level.dimensions
        t_width, t_height = self.ts_structures.tile_size
        c_width, c_height = pygame.display.get_window_size()
        center_x, center_y = c_width / 2, c_height / 2
        offset_x = center_x - (t_width * (l_width / 2))
        offset_y = center_y - (t_height * (l_height / 2))
        x, y = position
        position = (x * t_width) + offset_x, (y * t_height) + offset_y
        return position

    def _init_powerup(self, powerup) -> Powerup:
        position = powerup
        l_width, l_height = self.level.dimensions
        t_width, t_height = self.ts_structures.tile_size
        c_width, c_height = pygame.display.get_window_size()
        center_x, center_y = c_width / 2, c_height / 2
        offset_x = center_x - (t_width * (l_width / 2))
        offset_y = center_y - (t_height * (l_height / 2))
        x, y = position
        position = (x * t_width) + offset_x, (y * t_height) + offset_y
        return Powerup(position, (0, 0), self._powerup_black_heart)

    def _powerup_black_heart(self):
        self.player.subtract_love(5.0)

    def _powerup_heart(self):
        self.player.add_love(5.0)

    def manage_game_events(self) -> bool:
        """Manage the primary game events such as quitting, player movement, etc."""
        delta = self.frame_limiter.tick(self.fps) / 1000

        self.player.update_love()
        if self.player.love_meter <= 0:
            print("Player is out of love!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        pressed: Dict[int, bool] = pygame.key.get_pressed()
        self.player.update_position(pressed, delta, self.collidables)

        for entity in self.entities:
            if not entity.is_near(self.player):
                continue
            if not pressed[pygame.K_e]:
                continue
            if entity.fulfilled:
                continue

            self.player.subtract_love(0.5)
            entity.transfer(0.5)

            if entity.verify():
                self.game_over = True

        for powerup in self.powerups:
            powerup.activate_event(self.player)

        return not self.game_over

    def update_canvas(self) -> None:
        """Update the contents of the canvas."""

        # Fill the canvas with a black-like color.
        self.canvas.fill(self.palette.get_color("PINK"))

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
        for row_index, row in enumerate(self.level.tiles):

            # Fill in the tile with the appropriate tileset image at that position, or don't fill anything if the tile
            # is an "air" tile.
            for col_index, (cx, cy) in enumerate(row):
                if cx != -1 and cy != -1:
                    tile = self.ts_structures.get_tile(cx, cy)

                    # If this is the "first paint", get all of the tiles that are collidable and store their
                    # rectangles in the collidables list to help detect collisions for the player.
                    if not self.made_first_paint and self.level.is_collidable((row_index, col_index)):
                        self.collidables.append(
                            pygame.Rect(tile_x, tile_y, t_width, t_height)
                        )

                    self.canvas.blit(tile, (tile_x, tile_y))
                tile_x += t_width

            # Move to the next row and reset the X position.
            tile_y += t_height
            tile_x = offset_x

        # Repeat the same process for the decor layer.
        tile_x, tile_y = offset_x, offset_y
        for row in self.level.decor:
            for cx, cy in row:
                if cx != -1 and cy != -1:
                    self.canvas.blit(
                        self.ts_decor.get_tile(cx, cy), (tile_x, tile_y))
                tile_x += t_width
            tile_y += t_height
            tile_x = offset_x

        for powerup in self.powerups:
            if powerup.activated:
                continue
            self.canvas.blit(self.ts_structures.get_tile(
                0, 0), powerup.canvas_position)

        self.canvas.blit(self.ts_structures.get_tile(
            1, 0), self.player.position)

        for entity in self.entities:
            self.canvas.blit(self.ts_structures.get_tile(
                1, 0), entity.position)

    def render(self) -> None:
        """Render the changes onto the screen."""
        if not self.made_first_paint:
            self.made_first_paint = True
        pygame.display.update()

    def lifecycle(self):
        """Run a standard game lifecycle of handling game events, updating the canvas, and rendering the contents to the
            screen.

        Returns:
            A boolean whether the game should keep running.
        """
        should_keep_running = self.manage_game_events()
        self.update_canvas()
        self.render()
        return should_keep_running
