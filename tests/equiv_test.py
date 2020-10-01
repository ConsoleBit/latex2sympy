from .context import assert_equal
import hashlib
from sympy import Symbol

a = Symbol('a', real=True)
b = Symbol('b', real=True)


def test_open_equiv_letter():
    assert_equal("\\equivalence{\\variable{a},\\variable{b}}", Symbol('a', real=True) == Symbol('b', real=True))


def test_open_equiv_digit():
    assert_equal("\\equivalence{\\variable{5},\\variable{6}}", Symbol('5', real=True) == Symbol('6', real=True))
