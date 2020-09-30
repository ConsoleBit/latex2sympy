from sympy import Symbol, StrictLessThan, sin, LessThan, StrictGreaterThan, GreaterThan, Eq, Ne

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_lt_variable():
    assert_equal("\\variable{x}\\lt\\variable{y}", (Symbol('x', real=True) < Symbol('y', real=True)))


def test_lt_digit():
    assert_equal("4\\lt5", StrictLessThan(4, 5))


def test_lt_greek_letter():
    assert_equal("\\alpha\\lt\\beta", (Symbol('alpha', real=True) < Symbol('beta', real=True)))


def test_lt_trig():
    assert_equal("\\sin(90)\\lt\\sin(45)", StrictLessThan(sin(90), sin(45)))


def test_leq_variable():
    assert_equal("\\variable{x}\\leq\\variable{y}", (Symbol('x', real=True) <= Symbol('y', real=True)))


def test_leq_digit():
    assert_equal("4\\leq5", LessThan(4, 5))


def test_leq_greek_letter():
    assert_equal("\\alpha\\leq\\beta", (Symbol('alpha', real=True) <= Symbol('beta', real=True)))


def test_leq_trig():
    assert_equal("\\sin(90)\\leq\\sin(45)", LessThan(sin(90), sin(45)))


def test_gt_variable():
    assert_equal("\\variable{x}\\gt\\variable{y}", (Symbol('x', real=True) > Symbol('y', real=True)))


def test_gt_digit():
    assert_equal("4\\gt5", StrictGreaterThan(4, 5))


def test_gt_greek_letter():
    assert_equal("\\alpha\\gt\\beta", (Symbol('alpha', real=True) > Symbol('beta', real=True)))


def test_gt_trig():
    assert_equal("\\sin(90)\\gt\\sin(45)", StrictGreaterThan(sin(90), sin(45)))


def test_geq_variable():
    assert_equal("\\variable{x}\\geq\\variable{y}", (Symbol('x', real=True) >= Symbol('y', real=True)))


def test_geq_digit():
    assert_equal("4\\geq5", GreaterThan(4, 5))


def test_geq_greek_letter():
    assert_equal("\\alpha\\geq\\beta", (Symbol('alpha', real=True) >= Symbol('beta', real=True)))


def test_geq_trig():
    assert_equal("\\sin(90)\\geq\\sin(45)", GreaterThan(sin(90), sin(45)))


def test_eq_variable():
    assert_equal("\\variable{x}\\eq\\variable{y}", (Symbol('x', real=True) == Symbol('y', real=True)))


def test_eq_digit():
    assert_equal("4\\eq5", Eq(4, 5))


def test_eq_greek_letter():
    assert_equal("\\alpha\\eq\\beta", (Symbol('alpha', real=True) == Symbol('beta', real=True)))


def test_eq_trig():
    assert_equal("\\sin(90)\\eq\\sin(45)", Eq(sin(90), sin(45)))


def test_neq_variable():
    assert_equal("\\variable{x}\\neq\\variable{y}", (Symbol('x', real=True) != Symbol('y', real=True)))


def test_neq_digit():
    assert_equal("4\\neq5", Ne(4, 5))


def test_neq_greek_letter():
    assert_equal("\\alpha\\neq\\beta", (Symbol('alpha', real=True) != Symbol('beta', real=True)))


def test_neq_trig():
    assert_equal("\\sin(90)\\neq\\sin(45)", Ne(sin(90), sin(45)))
