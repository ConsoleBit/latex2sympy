from .context import assert_equal
import hashlib
from sympy import Symbol

p = Symbol('p', real=True)
x = Symbol('x', real=True)
y = Symbol('y', real=True)



def test_lopen_int_letter():
    assert_equal("\\variable{p}\\in<\\variable{x},\\variable{y}]", Symbol('x', real=True) < Symbol('p', real=True) <= Symbol('y', real=True))


def test_lopen_int_digit():
    assert_equal("\\variable{3}\\in<\\variable{0},\\variable{6}]", Symbol('0', real=True) < Symbol('3', real=True) <= Symbol('6', real=True))
