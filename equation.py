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
    latex[1] = [2, 3, 4, 5]  # Data from Database
    cond_expr = condition(latex_con)
    for latex[0] in latex[1]:
        cond = cond_expr.subs(iChild, latex[0])
        if cond:
            print("equation")


a = r"\variable{jChild}\for\variable{ChildContract}"  # jChild ∈ ChildContract (Iteration)
b = r"\neg{\variable{iChild}<4}"                      # iChild < 4             (Condition)
iteration(a, b)
