from sympy import Symbol, Not, And, Or

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_and_variable():
    assert_equal("\\and{\\variable{x},\\variable{y}}", Symbol('x', real=True) & Symbol('y', real=True))


def test_and_binary():
    assert_equal("\\and{1,0}", And(1, 0))


def test_or_variable():
    assert_equal("\\or{\\variable{x},\\variable{y}}", Symbol('x', real=True) | Symbol('y', real=True))


def test_or_binary():
    assert_equal("\\or{1,0}", Or(1, 0))


def test_not_variable():
    assert_equal("\\not{\\variable{x}}", Not(Symbol('x', real=True)))


def test_not_binary():
    assert_equal("\\not{0}", Not(0))
