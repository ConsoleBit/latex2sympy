from sympy import Symbol, Not

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_and_variable():
    assert_equal("\\and{\\variable{x},\\variable{y}}", Symbol('x', real=True) & Symbol('y', real=True))


def test_or_variable():
    assert_equal("\\or{\\variable{x},\\variable{y}}", Symbol('x', real=True) | Symbol('y', real=True))


def test_not_variable():
    assert_equal("\\not{\\variable{x}}", Not(Symbol('x', real=True)))

