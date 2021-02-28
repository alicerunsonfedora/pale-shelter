#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
from random import randint
from os import listdir
import pygame

from src.logic.state import GameState, GameStateManager
from src.logic.scene import GameScene
from src.logic.scenes import GameDriver, MainMenu, GameOver
from src.assets import asset_path


def max_levels():
    """Returns the maximum number of levels."""
    levels = sorted([level.replace(".lvl", "") for level in listdir(
        asset_path("data")) if level.startswith("random")])
    last_level = levels[-1:][0].replace("random", "")
    return int(last_level)


def pseudo_random_number(maximum_value, previous=1):
    """Returns a random number that isn't the previous value.

    Arguments:
        maximum_value (int): The highest number the random number can be.
        previous (int): The previous number to skip in the random picking. Defaults to 1.

    Returns:
        A random integer that is not the previous number.
    """
    val = randint(1, maximum_value)
    if val != previous:
        return val
    return pseudo_random_number(maximum_value, previous)


def main():
    """Execute the main game loop."""
    # Create the game object instance and a variable to control the loop.
    pygame.init()
    state_mgr = GameStateManager()
    state_mgr.state = GameState.MENU
    state_mgr.player_meter = 100.0

    pygame.mixer.music.load(asset_path("assets/audio/heartache.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    WINDOW = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("No Love")

    CLOCK = pygame.time.Clock()
    FPS = 60

    MAX_LEVEL = max_levels()
    PREVIOUS_LEVEL = 1

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
            PREVIOUS_LEVEL = pseudo_random_number(MAX_LEVEL, PREVIOUS_LEVEL)
            random_level = f"random{PREVIOUS_LEVEL:02d}"
            scene: GameScene = GameDriver(WINDOW, CLOCK, random_level, FPS)
            scene.player.love_meter = state_mgr.player_meter
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            state_mgr.player_meter = scene.player.love_meter
            if state_mgr.player_meter == 0.0:
                state_mgr.state = GameState.WIN
            elif scene.game_over:
                state_mgr.state = GameState.GAME_OVER

        # If the current state is game over, display the game over screen until the player presses a button.
        elif state_mgr.state == GameState.GAME_OVER:
            state_mgr.player_meter = 100.0
            scene: GameScene = GameOver(WINDOW, CLOCK, FPS)
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            if scene.action == "retry":
                state_mgr.state = GameState.IN_GAME
            else:
                state_mgr.state = GameState.MENU

        # If the player has won, show the winning screen.
        elif state_mgr.state == GameState.WIN:
            state_mgr.player_meter = 100.0
            scene: GameScene = GameOver(WINDOW, CLOCK, FPS, text="YOU WIN?")
            managed_loop = True
            while managed_loop:
                managed_loop = scene.lifecycle()
            if scene.action == "retry":
                state_mgr.state = GameState.IN_GAME
            else:
                state_mgr.state = GameState.MENU

    pygame.quit()


if __name__ == "__main__":
    main()
