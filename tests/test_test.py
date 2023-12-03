import pytest
from clickomania import main


def test_prison_mike_photo():
    assert main.bg_img == 'prison_mike.jpg', 'Should prison_mike.jpg'
