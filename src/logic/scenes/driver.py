#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from random import randint
from typing import Dict, List, Tuple
import pygame

from src.logic.player import Player
from src.logic.entity import NonPlayerEntity
from src.logic.powerup import Powerup
from src.logic.scene import GameScene
from src.data.levels import Level
from src.assets import Tilesheet, ColorPalette, asset_path


class GameDriver(GameScene):
    """The main application class for the game."""

    def __init__(self, window, clock, map_name, fps: int = 60) -> None:
        """Set up the game's canvas, colors, tilesheets, and event listeners."""
        super().__init__(window, clock, fps)
        self.palette.assign_color_name("METER_UPPER", "a3c255")
        self.palette.assign_color_name("METER_LOWER", "6fa341")

        self.tilesets = {
            "structure": Tilesheet(
                asset_path("assets/tilesets/struct01.png"), (48, 48), (9, 9)),
            "decor": Tilesheet(asset_path(
                "assets/tilesets/decor01.png"), (48, 48), (22, 24)),
            "powerups": Tilesheet(asset_path(
                "assets/tilesets/powerups.png"), (48, 48), (1, 2)),
            "ui": Tilesheet(asset_path("assets/ui/ui_master.png"), (48, 48), (12, 12))
        }

        self.level = Level(asset_path(f"data/{map_name}.lvl"))
        self.player = Player(self._init_entity_position("PLAYER"), 4)

        exit_x, exit_y = self.get_canvas_position(self.level.exit)
        self.exit_trigger = pygame.Rect(exit_x, exit_y, 48, 48)

        self.collidables = []
        self.made_first_paint = False

        self.entities: List[NonPlayerEntity] = []
        self.game_over = False

        for name, _ in self.level.entities:
            if name == "PLAYER":
                continue
            self.entities.append(NonPlayerEntity(
                name, self._init_entity_position(name)))

        self.powerups: List[Powerup] = []
        for powerup in self.level.powerups:
            self.powerups.append(self._init_powerup(powerup))

        self.love_meter_bg = pygame.image.load(
            asset_path("assets/ui/lovemeter.png"))

    def get_canvas_position(self, position) -> Tuple[int, int]:
        l_width, l_height = self.level.dimensions
        t_width, t_height = self.tilesets["structure"].tile_size
        c_width, c_height = pygame.display.get_window_size()
        center_x, center_y = c_width / 2, c_height / 2
        offset_x = center_x - (t_width * (l_width / 2))
        offset_y = center_y - (t_height * (l_height / 2))
        x, y = position
        c_position = (x * t_width) + offset_x, (y * t_height) + offset_y
        return c_position

    def _init_entity_position(self, entity) -> Tuple[int, int]:
        position = 0, 0
        for ent_name, ent_position in self.level.entities:
            if ent_name != entity:
                continue
            position = ent_position
            break
        return self.get_canvas_position(position)

    def _init_powerup(self, powerup) -> Powerup:
        position = self.get_canvas_position(powerup)
        random_seed = randint(1, 76)
        if random_seed >= 34:
            callback = self._powerup_heart
            texture = (0, 0)
        else:
            callback = self._powerup_black_heart
            texture = (1, 0)
        return Powerup(position, texture, callback)

    def _powerup_black_heart(self):
        self.player.subtract_love(5.0)

    def _powerup_heart(self):
        self.player.add_love(5.0)

    def manage_game_events(self) -> bool:
        """Manage the primary game events such as quitting, player movement, etc."""
        super().manage_game_events()

        self.player.update_love()
        if self.player.love_meter <= 0:
            print("Player is out of love!")

        pressed: Dict[int, bool] = pygame.key.get_pressed()
        self.player.update_position(pressed, self.delta, self.collidables)

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

        player_x, player_y = self.player.position
        if self.exit_trigger.collidepoint(player_x, player_y):
            return False

        return not self.game_over

    def update_canvas(self) -> None:
        """Update the contents of the canvas."""

        # Fill the canvas with a black-like color.
        super().update_canvas()
        self.canvas.fill(self.palette.get_color("DARK_BLACK"))

        # Get the width and the height of the level, tiles, and the window.
        l_width, l_height = self.level.dimensions
        t_width, t_height = self.tilesets["structure"].tile_size
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
                    tile = self.tilesets["structure"].get_tile(cx, cy)

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
                        self.tilesets["decor"].get_tile(cx, cy), (tile_x, tile_y))
                tile_x += t_width
            tile_y += t_height
            tile_x = offset_x

        self._draw_powerups()
        self._draw_entities()
        self._draw_lovemeter()

    def _draw_powerups(self):
        for powerup in self.powerups:
            tex_x, tex_y = powerup.texture_position
            if powerup.activated:
                continue
            self.canvas.blit(self.tilesets["powerups"].get_tile(
                tex_x, tex_y), powerup.canvas_position)

    def _draw_entities(self):
        for entity in self.entities:
            ex, ey = entity.position
            ey -= 48
            self.canvas.blit(entity.get_texture(), (ex, ey))

            if not entity.fulfilled:
                continue

            tx, ty = (6, 1) if entity.verify() else (7, 1)
            ui_y_offset = 4
            self.canvas.blit(
                self.tilesets["ui"].get_tile(tx, ty), (ex, ey - ui_y_offset))
            self.canvas.blit(
                self.tilesets["ui"].get_tile(tx, ty-1), (ex, ey - (ui_y_offset + 48)))

        px, py = self.player.position
        py -= 48
        self.canvas.blit(self.player.get_texture(), (px, py))

    def _draw_lovemeter(self):
        progress = 248 * (self.player.love_meter / 100)
        self.canvas.blit(self.love_meter_bg, (16, 16))
        pygame.draw.rect(self.canvas, self.palette.get_color(
            "METER_UPPER"), pygame.Rect(76, 40, progress, 8))
        pygame.draw.rect(self.canvas, self.palette.get_color(
            "METER_LOWER"), pygame.Rect(76, 48, progress, 8))

    def render(self) -> None:
        """Render the changes onto the screen."""
        if not self.made_first_paint:
            self.made_first_paint = True
        super().render()
