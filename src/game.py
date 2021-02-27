#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from src.logic.state import GameState, GameStateManager
import pygame
from src.logic import GameDriver

pygame.init()


def main():
    """Execute the main game loop."""
    # Create the game object instance and a variable to control the loop.
    state_mgr = GameStateManager()
    state_mgr = GameState.IN_GAME

    WINDOW = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("No Love")

    CLOCK = pygame.time.Clock()
    FPS = 60

    game = GameDriver(WINDOW, CLOCK, fps=FPS)

    in_game = True

    # Manage the game events, update the canvas, and render.
    while in_game:
        in_game = game.lifecycle()

    pygame.quit()


if __name__ == "__main__":
    main()
