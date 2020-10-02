from sympy import Symbol, StrictLessThan, sin, LessThan, StrictGreaterThan, GreaterThan, Eq, Ne

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_union_variable():
    assert_equal("\\variable{x}\\cup\\variable{y}", set().union({'x'}, {'y'}))


def test_intersection_variable():
    assert_equal("\\variable{x}\\cap\\variable{y}", set().intersection({'x'}, {'y'}))

def test_subset_variable():
    assert_equal("\\variable{x}\\subseteq\\variable{y}", ({'x'}).issubset({'y'}))

def test_superset_variable():
    assert_equal("\\variable{x}\\supseteq\\variable{y}", ({'x'}).issuperset({'y'}))

def test_belongsto_variable():
    assert_equal("\\variable{x}\\in\\variable{y}", 'x' in {'y'})

def test_notin_variable():
    assert_equal("\\variable{x}\\notin\\variable{y}", 'x' not in {'y'})
