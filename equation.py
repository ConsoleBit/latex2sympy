from sympy import Symbol

import latex2sympy

iChild = Symbol('iChild', real=True)
jChild = Symbol('jChild', real=True)
ChildContract = Symbol('ChildContract', real=True)


def condition(latex_con):
    latex = latex2sympy.process_sympy(latex_con)
    print(latex)
    return latex


def iteration(latex_iter, latex_con):
    latex = latex2sympy.process_sympy(latex_iter)

    cond_expr = condition(latex_con)
    for latex[0] in latex[1]:  # for jChild in ChildContract (dynamic)
        cond = cond_expr.subs(iChild, latex[0])  # (iChild<4).subs(iChild, jChild)
        if cond:
            latex2sympy.process_sympy(r"\sum_{\variable{d} = 1}^{3} \variable{d}*\variable{ENERGY} ")


a = r"\sum_{\variable{jChild} = \variable{Childcontracts}}^{\variable{Childcon}} (\variable{x}+\variable{y})"  # jChild ∈ ChildContract (Iteration)
b = r"\lor{\len{\variable{x}}<5,\variable{y}<3}}"                        # (len(x) < 5) | (y < 3)             (Condition)
iteration(a, b)





