#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
from random import randint
import pygame

from src.logic.state import GameState, GameStateManager
from src.logic.scene import GameScene
from src.logic.scenes import GameDriver, MainMenu, GameOver
from src.assets import asset_path


def main():
    """Execute the main game loop."""
    # Create the game object instance and a variable to control the loop.
    pygame.init()
    state_mgr = GameStateManager()
    state_mgr.state = GameState.MENU
    state_mgr.player_meter = 100.0

    pygame.mixer.music.load(asset_path("assets/audio/heartache.mp3"))
    pygame.mixer.music.play(-1)

    WINDOW = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("No Love")

    CLOCK = pygame.time.Clock()
    FPS = 60

    while state_mgr.state != GameState.EXIT:
        # If the current state is the main menu, display it until the player clicks a button.
        if state_mgr.state == GameState.MENU:
            scene: GameScene = MainMenu(WINDOW, CLOCK, FPS)
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            if scene.action == "start":
                state_mgr.state = GameState.IN_GAME
            else:
                state_mgr.state = GameState.EXIT

        # If the current state is in-game, load a level and keep running until the player loses.
        elif state_mgr.state == GameState.IN_GAME:
            random_level = f"random0{randint(1, 2)}"
            scene: GameScene = GameDriver(WINDOW, CLOCK, random_level, FPS)
            scene.player.love_meter = state_mgr.player_meter
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            state_mgr.player_meter = scene.player.love_meter
            if scene.game_over:
                state_mgr.state = GameState.GAME_OVER

        # If the current state is game over, display the game over screen until the player presses a button.
        elif state_mgr.state == GameState.GAME_OVER:
            scene: GameScene = GameOver(WINDOW, CLOCK, FPS)
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            if scene.action == "retry":
                state_mgr.state = GameState.IN_GAME
                state_mgr.player_meter = 100.0
            else:
                state_mgr.state = GameState.MENU

    pygame.quit()


if __name__ == "__main__":
    main()
