from sympy import Pow, Symbol

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_nrt_variable():
    assert_equal("\\nrt{\\variable{x},\\variable{y}}", Pow(Symbol('x', real=True), 1 / Symbol('y', real=True)))


def test_nrt_digit():
    assert_equal("\\nrt{8,3}", Pow(8, 1 / 3))


def test_nrt_greek_letter():
    assert_equal("\\nrt{\\alpha,\\beta}", Pow(Symbol('alpha', real=True), 1 / Symbol('beta', real=True)))
