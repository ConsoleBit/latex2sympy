from .context import assert_equal
import hashlib
from sympy import Symbol

x = Symbol('x', real=True)


def test_open_interval_letter():
    assert_equal("\\absolute\\variable{x}", Symbol('x' + hashlib.md5('x'.encode()).hexdigest(), real=True))


def test_open_interval_digit():
    assert_equal("\\absolute\\variable{4}", Symbol('4' + hashlib.md5('4'.encode()).hexdigest(), real=True))
