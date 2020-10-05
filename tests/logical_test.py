from sympy import Symbol, Not, And, Or

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_and_variable():
    assert_equal("\\land{\\variable{x},\\variable{y}}", Symbol('x', real=True) & Symbol('y', real=True))


def test_and_binary():
    assert_equal("\\land{1,0}", And(1, 0))


def test_or_variable():
    assert_equal("\\lor{\\variable{x},\\variable{y}}", Symbol('x', real=True) | Symbol('y', real=True))


def test_or_binary():
    assert_equal("\\lor{1,0}", Or(1, 0))


def test_not_variable():
    assert_equal("\\neg{\\variable{x}}", Not(Symbol('x', real=True)))


def test_not_binary():
    assert_equal("\\neg{0}", Not(0))
