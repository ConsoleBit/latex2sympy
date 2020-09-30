from sympy import symbols, pi

import latex2sympy

x, y, z = symbols('x,y,z')
a, b, c = symbols('a b c')


# a = "ImageSet(Lambda(_n, _n*pi + pi/12), Integers) \ Union(ImageSet(Lambda(_n, 2*_n*pi + 5*pi/4), Integers)"
# a = r"\subset"
# a = r"{x}\cap ({y}\cup {z})$"
# a = r"\pi"
# a = r"\emptyset"
# a = r"\infty"
# a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"
# a = r"e^5"
# a = r"3\in\left\{1,2,3,4,5\right\}"
# a = "{9,14} ⊂ {9,14,28}"
# a = r"\variable{b},\variable{a}"
# a = r"\union{\variable{p,p,q,1}}"

# a = r"\iterator{\epsilon{\variable{a},\variable{b}}\condition{}}"

# a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{p}\lt\variable{q}"

# a = r"\epsilon{\variable{p},\variable{q,p}}"
#
# a = r"\pi\gt6"
#
# a = r"\variable{p}\leq\variable{q}"
#
# a = r"\variable{p}\gt\variable{q}"
#
# a = r"\variable{p}\geq\variable{q}"
#
# a = r"\lcm(\variable{x}, \variable{y})\eq\lcm(\variable{a}, \variable{b})"

# a = r"\lcm(\variable{x}, \variable{y})"
#
# a = r"\variable{p}\neq\variable{q}"
#
# a = r"0\and0"

# a = r"\variable{p}\or\variable{q}"

# a = r"\frac{8}{2}"

# a = r"20\per_thousand"

# a = r"\variable{a}+\variable{b}"
# a = r"\superset{\variable{p},\variable{q}}"

# a = r"\variable{p}\open_int\variable{x}\variable{y}"
# a = r"\absolute\variable{x}"
# a = r"\union{\variable{x},\variable{y}}"
# a = r"\variable{\\alpha}"

# a = r"\nrt{8,3}"
# sympy.Pow(symbol[0],1/symbol[1]).subs({symbol[0]:8,symbol[1]:3})

# a = r"\begin{matrix}1 & 2 & 3\\a & b & c\end{matrix}"

a = r"\not{\variable{x}}"

res = latex2sympy.process_sympy(a)
print('Result: ', res)



# print(res._eval_relation(pi,1))

# for i in b.free_symbols:
#     if "_" in i.name:
#         variable, dimension = i.name.split('_')
#         dimension = dimension[1: len(dimension) - 1]
#         dimension = dimension.split(",")
#         print("Variable", variable, ", Dimension", dimension)
# print(res.evalf(1))

# from sympy.logic.boolalg import as_Boolean
#
#
# a = 1
# b = 2
# c = 3
# e = a + b > b - c
# a = as_Boolean(e)
# print(a)
#
#
# from sympy import symbols, S, pprint, solveset
# x,y, n = symbols('y,x, n')
# pprint(solveset(abs(x) - n, x, domain=S.Reals), use_unicode=True)
#
#
# from sympy import ConditionSet, Eq, Symbol, Interval, srepr
#
# x=Symbol('x')
# s=ConditionSet(x, Eq(x**2-2*x,0), Interval(1,10))
# s
# print(s)
#
# from sympy.parsing.latex import parse_latex
# e = r"\frac{4}{5}"
# print (srepr(e))


# lis = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5}, {4, 5}, {6}]


# lis = set()
# lis = {1, 2, 3, 4, 5, 6, 6, 7}
# a = set()
# a = {9, 2, 3, 4}
#

# sympy.And(True,True)

