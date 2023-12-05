import pytest
import pygame
from clickomania import main


def test_get_color():
    t_color = main.get_color()
    assert t_color in main.COLORS, 'Color should be in COLORS list'


def test_game_field():
    pass