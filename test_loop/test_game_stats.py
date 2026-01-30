import pytest
from game_stats import Game

def test_ratio():
    # Normal case
    g = Game(100, 2)
    assert g.get_ratio() == 50.0

def test_zero_division():
    # Edge case: The Fixer MUST prevent a crash
    g = Game(100, 0)
    # If it crashes, the test fails. 
    # If it returns None or 0, the test passes.
    try:
        result = g.get_ratio()
        assert result == 0 or result is None
    except ZeroDivisionError:
        assert False, "Code crashed on division by zero"