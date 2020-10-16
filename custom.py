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



def find_square(x):
    return x ** 2

def cand(x,y):
    return x and y


helper_functions = {
    "len": len,
    "suqaure": find_square,
    "and": cand
}



# a = r"\frac{\sum_{\variable{ExchRt_{\variable{xday}}} = 1}^{31} \variable{jain}\variable{ExchRt_{\variable{xday}}}}{\len{\variable{DaysInMonth}}}"
# a = r"(\cand{\variable{x}\,\variable{y}})>1"
a = r" \variable{a}+\variable{DEMO_{\variable{iab_{\variable{x_{\variable{y}}},\variable{z}}}}}"
# a = r"\lor{\variable{a}<\variable{b},\variable{c}>0}"


demo = latex2sympy.process_sympy(a)
print(demo)
print(demo.free_symbols)
for j in demo.args:
    for i in j.free_symbols:
        for a in helper_functions.keys():
            if a in i.name:
                if '(' in i.name:
                    fun, val = i.name.split('(')
                    arg = val.split(')')[0]
                    # from db get value of y
                    val = [1,2]
                    test = demo.replace(i,helper_functions[fun](val))
                    print(test)
                else:
                    fun, val = (i.name).split(a)
                    test = demo.replace(i, helper_functions[a](fun,val))




