from .context import assert_equal
import hashlib
from sympy import Symbol

a = Symbol('a', real=True)
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)



def test_open_sum_letter():
    assert_equal("\\summation{\\variable{a},\\variable{x},\\variable{y},\\variable{z}}",
                 Symbol('a', real=True) * Symbol('y', real=True) + Symbol('z', real=True) - Symbol('x', real=True))
