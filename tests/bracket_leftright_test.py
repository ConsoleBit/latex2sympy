from .context import assert_equal, _Pow
import pytest
from sympy import Integral, sin, Symbol, Mul, Integer, Pow
from latex2sympy.latex2sympy import process_sympy

a = Symbol('a', real=True)
b = Symbol('b', real=True)
x = Symbol('x', real=True)
theta = Symbol('theta', real=True)


def test_bracket_none():
    assert_equal("\\int x dx", Integral(x, x))


def test_bracket_paren():
    assert_equal("\\sin(\\theta)", sin(theta))


def test_bracket_leftright_paren():
    assert_equal("\\sin\\left(\\theta\\right)", sin(theta))


def test_brackets():
    assert_equal("\\sin{\\theta}", sin(theta))


def test_bracket_leftright():
    assert_equal("\\sin\\left{\\theta\\right}", sin(theta))


def test_bracket_mixed():
    assert_equal("\\frac{1}{2}ab(a+b)", Mul(_Pow(2, -1), a, b, (a + b), evaluate=False))
