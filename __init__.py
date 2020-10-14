from sympy import Symbol

import latex2sympy

x = Symbol('x', real=True)
y = Symbol('y', real=True)
fi = Symbol('fi', real=True)
Childcontracts = Symbol('Childconracts', real=True)
Childcon = Symbol('Childcon', real=True)

# a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"

# a = r"\lor{\variable{x},\variable{y}}>\lor{\variable{x},\variable{y}}"

# a = r"\sum_{\variable{jChild} = 2}^4 (\variable{x}+\variable{y}+\variable{jChild})"

a = r"1 + \variable{a}+\variable{DEMO_{\variable{i_{\variable{x_{\variable{y}}},\variable{z}}}}}"

b = latex2sympy.process_sympy(a)
print(b)
