"""The pyinst module contains utility functions for use with PyInstaller."""
import os
import sys


def asset_path(relative):
    """Returns the asset path for a given file in Pygame.

    This is commonly used to get an asset when it can't be easily located in a packaged app via PyInstaller. Use this
        instead of calling the asset path directly.

    Original function was created by Irwin Kwan at 
        https://irwinkwan.com/2013/04/29/python-executables-pyinstaller-and-a-48-hour-game-design-compo/. Many thanks.

    Arguments:
        relative (str): The filepath to the asset to get.

    Returns:
        The filepath with corrections for PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, *relative.split("/"))
    return os.path.join(relative)
