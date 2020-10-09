from sympy import Symbol, Union, Interval, Abs, Add
from sympy.functions.elementary.complexes import length

import latex2sympy

x = Symbol('x', real=True)
y = Symbol('y', real=True)

# a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"

# a = r"\variable{x}+1>\neg{\neg{\variable{x}}}>\lor{\neg{\variable{y}},\variable{x}}"
# a = r"\lor{\variable{x},\variable{y}}>\lor{\variable{x},\variable{y}}"
# a = r"\variable{a}\cup\variable{b}"

# print(Union(Interval(x,y),Interval(x,y)))
# Abs(x)
#
# a = r"(\lor{\variable{x},\variable{y}})>2"
# b = latex2sympy.process_sympy(a)
# print(b)

print(Abs(x))


# for i in b.free_symbols:
#     if "_" in i.name:
#         variable, dimension = i.name.split('_')
#         dimension = dimension[1: len(dimension) - 1]
#         dimension = dimension.split(",")
#         print("Variable", variable, ", Dimension", dimension)
# print(b.evalf(1))
