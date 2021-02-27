#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
from src.assets.pyinst import asset_path
from src.assets.color import ColorPalette
import pygame
import sys


class GameScene():
    def __init__(self, window, clock, fps=60):
        self.canvas = window
        self.frame_limiter = clock
        self.fps = fps
        self.delta = 0

        self.palette = ColorPalette(asset_path(
            "assets/palettes/nostalgia36.gpl"))
        self.palette.assign_color_name("DARK_BLACK", "1e2029")

    def manage_game_events(self) -> bool:
        self.delta = self.frame_limiter.tick(self.fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        return True

    def update_canvas(self):
        pass

    def render(self):
        pygame.display.update()

    def lifecycle(self):
        resp = self.manage_game_events()
        self.update_canvas()
        self.render()
        return resp
