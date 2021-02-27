#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
from random import randint
import pygame
from src.logic.state import GameState, GameStateManager
from src.logic.scene import GameScene
from src.logic.scenes import GameDriver, MainMenu


def main():
    """Execute the main game loop."""
    # Create the game object instance and a variable to control the loop.
    pygame.init()
    state_mgr = GameStateManager()
    state_mgr.state = GameState.MENU

    WINDOW = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("No Love")

    CLOCK = pygame.time.Clock()
    FPS = 60

    while state_mgr.state != GameState.EXIT:
        if state_mgr.state == GameState.MENU:
            scene: GameScene = MainMenu(WINDOW, CLOCK, FPS)
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            if scene.action == "start":
                state_mgr.state = GameState.IN_GAME
            else:
                state_mgr.state = GameState.EXIT
        if state_mgr.state == GameState.IN_GAME:
            random_level = f"random0{randint(1, 2)}"
            scene: GameScene = GameDriver(WINDOW, CLOCK, random_level, FPS)
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            if scene.game_over:
                state_mgr.state = GameState.GAME_OVER
        if state_mgr.state == GameState.GAME_OVER:
            state_mgr.state = GameState.EXIT

    pygame.quit()


if __name__ == "__main__":
    main()
