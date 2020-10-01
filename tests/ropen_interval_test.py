from .context import assert_equal
import hashlib
from sympy import Symbol

p = Symbol('p', real=True)
x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_ropen_int_letter():
    assert_equal("\\variable{p}\\ropen_int\\variable{x}\\variable{y}",
                 Symbol('x' + hashlib.md5('x'.encode()).hexdigest(), real=True) <= Symbol(
                     'p' + hashlib.md5('p'.encode()).hexdigest(), real=True) < Symbol(
                     'y' + hashlib.md5('y'.encode()).hexdigest(), real=True))


def test_ropen_int_digit():
    assert_equal("\\variable{3}\\ropen_int\\variable{0}\\variable{6}",
                 Symbol('0' + hashlib.md5('0'.encode()).hexdigest(), real=True) <= Symbol(
                     '3' + hashlib.md5('3'.encode()).hexdigest(), real=True) < Symbol(
                     '6' + hashlib.md5('6'.encode()).hexdigest(), real=True))
