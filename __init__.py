from sympy import symbols, pi

import latex2sympy

x, y, z = symbols('x,y,z')
a, b, c = symbols('a b c')

a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"

res = latex2sympy.process_sympy(a)
print('Result: ', res)

for i in b.free_symbols:
    if "_" in i.name:
        variable, dimension = i.name.split('_')
        dimension = dimension[1: len(dimension) - 1]
        dimension = dimension.split(",")
        print("Variable", variable, ", Dimension", dimension)
print(res.evalf(1))
