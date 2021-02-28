#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import pygame
from src.logic import scene
from src.assets import asset_path


class MainMenu(scene.GameScene):
    """The scene class responsible for handling main menu functions to start and quit the game."""

    def __init__(self, window, clock, fps):
        super().__init__(window, clock, fps=fps)
        self.palette.assign_color_name("TITLE_COLOR", "c1cada")
        self.action = ""
        self.logo = pygame.image.load(asset_path("assets/logo.png"))
        self.title_font = pygame.font.Font(
            asset_path("assets/fonts/Forum-Regular.ttf"), 72)
        self.regular_font = pygame.font.Font(
            asset_path("assets/fonts/Forum-Regular.ttf"), 32)

        self._htp_size = 192, 256

        self.title_text = self.title_font.render(
            "NO LOVE", True, self.palette.get_color("TITLE_COLOR"))
        self.start_button = self.regular_font.render(
            "START GAME", True, (255, 255, 255))
        self.quit_button = self.regular_font.render(
            "QUIT", True, (255, 255, 255))
        self.start_rect = self.start_button.get_rect()
        self.quit_rect = self.quit_button.get_rect()

        self.how_to_play_images = {
            "left": pygame.image.load(asset_path("assets/ui/htp_1.png")),
            "right": pygame.image.load(asset_path("assets/ui/htp_2.png"))
        }

    def manage_game_events(self) -> bool:
        super().manage_game_events()
        clicked = pygame.mouse.get_pressed()
        if clicked[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_rect.collidepoint(mouse_pos):
                self.action = "start"
                return False
            elif self.quit_rect.collidepoint(mouse_pos):
                self.action = "quit"
                return False
        return True

    def update_canvas(self):
        super().update_canvas()
        window_width, window_height = pygame.display.get_window_size()
        h_width, h_height = window_width / 2, window_height / 2
        self.canvas.fill(self.palette.get_color("DARK_BLACK"))

        logo_x_pos = h_width - (self.logo.get_rect().width / 2)
        self.canvas.blit(self.logo, (logo_x_pos, 128))

        title_x_pos = h_width - (self.title_text.get_rect().width / 2)
        self.canvas.blit(self.title_text, (title_x_pos,
                                           136 + self.logo.get_rect().height))

        self.start_rect.x = start_x_pos = h_width - \
            (self.start_button.get_rect().width / 2)
        self.start_rect.y = start_y_pos = h_height + 100
        self.canvas.blit(self.start_button, (start_x_pos, start_y_pos))

        self.quit_rect.x = quit_x_pos = h_width - \
            (self.quit_button.get_rect().width / 2)
        self.quit_rect.y = quit_y_pos = h_height + 116 + self.start_rect.height
        self.canvas.blit(self.quit_button, (quit_x_pos, quit_y_pos))

        htp_padding = 32
        htp_width, htp_height = self._htp_size
        controls_y = h_height - (htp_height / 2)
        self.canvas.blit(
            self.how_to_play_images["left"], (htp_padding, controls_y))

        gameplay_x = window_width - htp_width - htp_padding
        self.canvas.blit(
            self.how_to_play_images["right"], (gameplay_x, controls_y))
