#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import pygame
from src.logic.scene import GameScene
from src.assets import asset_path


class GameOver(GameScene):
    """The scene class for handling the UI when the game is over."""

    def __init__(self, window, clock, fps):
        super().__init__(window, clock, fps=fps)
        self.action = ""

        self.title_font = pygame.font.Font(
            asset_path("assets/fonts/Forum-Regular.ttf"), 72)
        self.regular_font = pygame.font.Font(
            asset_path("assets/fonts/Forum-Regular.ttf"), 32)

        self.title_text = self.title_font.render(
            "GAME OVER!", True, (255, 255, 255))
        self.retry_button = self.regular_font.render(
            "RETRY", True, (255, 255, 255))
        self.menu_button = self.regular_font.render(
            "MAIN MENU", True, (255, 255, 255))
        self.retry_rect = self.retry_button.get_rect()
        self.menu_rect = self.menu_button.get_rect()

    def manage_game_events(self) -> bool:
        super().manage_game_events()
        clicked = pygame.mouse.get_pressed()
        if clicked[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.retry_rect.collidepoint(mouse_pos):
                self.action = "start"
                return False
            elif self.menu_rect.collidepoint(mouse_pos):
                self.action = "menu"
                return False
        return True

    def update_canvas(self):
        super().update_canvas()
        window_width, window_height = pygame.display.get_window_size()
        self.canvas.fill(self.palette.get_color("DARK_BLACK"))

        title_x_pos = (window_width / 2) - \
            (self.title_text.get_rect().width / 2)
        self.canvas.blit(self.title_text, (title_x_pos, 300))

        self.retry_rect.x = retry_x_pos = (window_width / 2) - \
            (self.retry_button.get_rect().width / 2)
        self.retry_rect.y = retry_y_pos = (window_height / 2) + 100
        self.canvas.blit(self.retry_button, (retry_x_pos, retry_y_pos))

        self.menu_rect.x = menu_x_pos = (window_width / 2) - \
            (self.menu_button.get_rect().width / 2)
        self.menu_rect.y = menu_y_pos = (
            window_height / 2) + 116 + self.retry_rect.height
        self.canvas.blit(self.menu_button, (menu_x_pos, menu_y_pos))
