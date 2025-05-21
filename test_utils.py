import pytest
from utils import add

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_mixed_sign_numbers():
    assert add(-2, 3) == 1

def test_add_zero():
    assert add(0, 5) == 5

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (1.5, 2.5, 4.0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
