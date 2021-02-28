#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The scene module provides the scene class that all game scenes derive from."""

from src.assets.pyinst import asset_path
from src.assets.color import ColorPalette
import pygame
import sys


class GameScene():
    """A class that represents a scene in the game.

    Class Attributes:
        canvas (Surface): The game window that is being displayed to the player.
        frame_limiter (Clock): The game's internal clock.
        fps (int): The maximum number of frames per second.
        delta (float): The change in time from the previous frame. Calculated on every frame.
        palette (ColorPalette): The color palette that can be used to fill the screen or draw elements manually.
    """

    def __init__(self, window, clock, fps=60):
        """Initialize the game scene.

        Arguments:
            window (Surface): The window the game scene will be rendered to.
            clock (Clock): The clock to handle game timing.
            fps (int): The maximum number of frames per second that the clock will force.
        """
        self.canvas = window
        self.frame_limiter = clock
        self.fps = fps
        self.delta = 0

        self.palette = ColorPalette(asset_path(
            "assets/palettes/nostalgia36.gpl"))
        self.palette.assign_color_name("DARK_BLACK", "1e2029")

    def manage_game_events(self) -> bool:
        """Calculate the delta from the previous frame and listen for game events.

        Classes that inherit the GameScene class should override this method and call the parent method to listen for
            quit event.

        Returns:
            Whether the scene should still be rendered to the screen.
        """
        self.delta = self.frame_limiter.tick(self.fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_m]:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(-1)
        return True

    def update_canvas(self):
        """Update the contents of the canvas to be rendered to the screen.

        Classes that inherit the GameScene class should override this method.
        """
        pass

    def render(self):
        """Render the contents of the canbas to the screen.

        Classes that inherit the GameScene class should override this method and call the parent method to ensure the
            changes get renedered to the screen.
        """
        pygame.display.update()

    def lifecycle(self):
        """Execute the lifecycle of a game scene once.

        A lifecycle would include managing the game events, updating the canvas, and then rendering those changes to the
            screen.

        Returns:
            Whether the scene should be rendered for the next lifecycle run.
        """
        resp = self.manage_game_events()
        self.update_canvas()
        self.render()
        return resp
