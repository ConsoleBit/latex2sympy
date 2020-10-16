from sympy import Symbol

import latex2sympy

x = Symbol('x', real=True)
y = Symbol('y', real=True)
fi = Symbol('fi', real=True)
d = Symbol('d', real=True)
ENERGY = Symbol('ENERGY', real=True)
Childcon = Symbol('Childcon', real=True)

# a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"

# a = r"\lor{\variable{x},\variable{y}}>\lor{\variable{x},\variable{y}}"

# a = r"1 + \variable{a}+\variable{DEMO_{\variable{i_{\variable{x_{\variable{y}}},\variable{z}}}}}"

# a = r"\frac{\sum_{\variable{ExchRt_{\variable{xday}}} = 1}^{31} \variable{EQUATION}\variable{ExchRt_{\variable{xday}}}}{\len{\variable{DaysInMonth}}}"

# a = r"\lor{\variable{a}<\variable{b},\variable{c}>0}"

a = r"\land{\variable{a},\variable{b}>5}"

demo = latex2sympy.process_sympy(a)
print(demo)
