#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import pygame
from src.logic import PaleShelter

pygame.init()


def main():
    """Execute the main game loop."""
    # Create the game object instance and a variable to control the loop.
    game = PaleShelter()
    in_game = True

    # Manage the game events, update the canvas, and render.
    while in_game:
        in_game = game.lifecycle()

    pygame.quit()


if __name__ == "__main__":
    main()
