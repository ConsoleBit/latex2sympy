from sympy import Symbol

import latex2sympy

x = Symbol('x', real=True)
y = Symbol('y', real=True)

a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"

b = latex2sympy.process_sympy(a)
print(b)

for i in b.free_symbols:
    if "_" in i.name:
        variable, dimension = i.name.split('_')
        dimension = dimension[1: len(dimension) - 1]
        dimension = dimension.split(",")
        print("Variable", variable, ", Dimension", dimension)
print(b.evalf(1))


