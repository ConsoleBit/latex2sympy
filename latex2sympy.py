import antlr4
import sympy
from antlr4.error.ErrorListener import ErrorListener
from sympy.core.numbers import Zero, One
from sympy.logic.boolalg import And, Not, BooleanFalse, BooleanTrue

try:
    from gen.PSParser import PSParser
    from gen.PSLexer import PSLexer
    from gen.PSListener import PSListener
except Exception:
    from .gen.PSParser import PSParser
    from .gen.PSLexer import PSLexer
    from .gen.PSListener import PSListener

from sympy.printing.str import StrPrinter

from sympy.parsing.sympy_parser import parse_expr

VARIABLE_VALUES = {}


def process_sympy(sympy, variable_values={}):
    # variable values
    global VARIABLE_VALUES
    if len(variable_values) > 0:
        VARIABLE_VALUES = variable_values
    else:
        VARIABLE_VALUES = {}

    # setup listener
    matherror = MathErrorListener(sympy)

    # stream input
    stream = antlr4.InputStream(sympy)
    lex = PSLexer(stream)
    lex.removeErrorListeners()
    lex.addErrorListener(matherror)

    tokens = antlr4.CommonTokenStream(lex)
    parser = PSParser(tokens)

    # remove default console error listener
    parser.removeErrorListeners()
    parser.addErrorListener(matherror)

    # process the input
    return_data = None
    math = parser.math()

    # if a list
    if math.relation_list():
        return_data = []

        # go over list items
        relation_list = math.relation_list().relation_list_content()
        for list_item in relation_list.relation():
            expr = convert_relation(list_item)
            return_data.append(expr)

    # if not, do default
    else:
        relation = math.relation()
        return_data = convert_relation(relation)

    return return_data


class MathErrorListener(ErrorListener):
    def __init__(self, src):
        super(ErrorListener, self).__init__()
        self.src = src

    def syntaxError(self, recog, symbol, line, col, msg, e):
        fmt = "%s\n%s\n%s"
        marker = "~" * col + "^"

        if msg.startswith("missing"):
            err = fmt % (msg, self.src, marker)
        elif msg.startswith("no viable"):
            err = fmt % ("I expected something else here", self.src, marker)
        elif msg.startswith("mismatched"):
            names = PSParser.literalNames
            expected = [names[i] for i in e.getExpectedTokens() if i < len(names)]
            if len(expected) < 10:
                expected = " ".join(expected)
                err = (fmt % ("I expected one of these: " + expected,
                              self.src, marker))
            else:
                err = (fmt % ("I expected something else here", self.src, marker))
        else:
            err = fmt % ("I don't understand this", self.src, marker)
        raise Exception(err)


def convert_relation(rel):
    if rel.expr():
        return convert_expr(rel.expr())

    lh = convert_relation(rel.relation(0))
    rh = convert_relation(rel.relation(1))
    if rel.LT():
        return sympy.StrictLessThan(lh, rh)
    elif rel.LTE():
        return sympy.LessThan(lh, rh, evaluate=False)
    elif rel.GT():
        return sympy.StrictGreaterThan(lh, rh, evaluate=False)
    elif rel.GTE():
        return sympy.GreaterThan(lh, rh, evaluate=False)
    elif rel.EQUAL():
        return sympy.Eq(lh, rh, evaluate=False)
    elif rel.UNEQUAL():
        return sympy.Ne(lh, rh, evaluate=False)


def convert_expr(expr):
    if expr.additive():
        return convert_add(expr.additive())


def convert_matrix(matrix):
    # build matrix
    row = matrix.matrix_row()
    tmp = []
    rows = 0
    for r in row:
        tmp.append([])
        for expr in r.expr():
            tmp[rows].append(convert_expr(expr))
        rows = rows + 1

    # return the matrix
    return sympy.Matrix(tmp)


def add_flat(lh, rh):
    if hasattr(lh, 'is_Add') and lh.is_Add or hasattr(rh, 'is_Add') and rh.is_Add:
        args = []
        if hasattr(lh, 'is_Add') and lh.is_Add:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_Add') and rh.is_Add:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.Add(*args, evaluate=False)
    else:
        return sympy.Add(lh, rh, evaluate=False)


def mat_add_flat(lh, rh):
    if hasattr(lh, 'is_MatAdd') and lh.is_MatAdd or hasattr(rh, 'is_MatAdd') and rh.is_MatAdd:
        args = []
        if hasattr(lh, 'is_MatAdd') and lh.is_MatAdd:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_MatAdd') and rh.is_MatAdd:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.MatAdd(*args, evaluate=False)
    else:
        return sympy.MatAdd(lh, rh, evaluate=False)


def mul_flat(lh, rh):
    if hasattr(lh, 'is_Mul') and lh.is_Mul or hasattr(rh, 'is_Mul') and rh.is_Mul:
        args = []
        if hasattr(lh, 'is_Mul') and lh.is_Mul:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_Mul') and rh.is_Mul:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.Mul(*args, evaluate=False)
    else:
        return sympy.Mul(lh, rh, evaluate=False)


def mat_mul_flat(lh, rh):
    if hasattr(lh, 'is_MatMul') and lh.is_MatMul or hasattr(rh, 'is_MatMul') and rh.is_MatMul:
        args = []
        if hasattr(lh, 'is_MatMul') and lh.is_MatMul:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_MatMul') and rh.is_MatMul:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.MatMul(*args, evaluate=False)
    else:
        return sympy.MatMul(lh, rh, evaluate=False)


def convert_add(add):
    if add.ADD():
        lh = convert_add(add.additive(0))
        rh = convert_add(add.additive(1))

        if lh.is_Matrix or rh.is_Matrix:
            return mat_add_flat(lh, rh)
        else:
            return add_flat(lh, rh)
    elif add.SUB():
        lh = convert_add(add.additive(0))
        rh = convert_add(add.additive(1))

        if lh.is_Matrix or rh.is_Matrix:
            return mat_add_flat(lh, mat_mul_flat(-1, rh))
        else:
            # If we want to force ordering for variables this should be:
            # return Sub(lh, rh, evaluate=False)
            if not rh.is_Matrix and rh.func.is_Number:
                rh = -rh
            else:
                rh = mul_flat(-1, rh)
            return add_flat(lh, rh)
    else:
        return convert_mp(add.mp())


def convert_mp(mp):
    if hasattr(mp, 'mp'):
        mp_left = mp.mp(0)
        mp_right = mp.mp(1)
    else:
        mp_left = mp.mp_nofunc(0)
        mp_right = mp.mp_nofunc(1)

    if mp.MUL() or mp.CMD_TIMES() or mp.CMD_CDOT():
        lh = convert_mp(mp_left)
        rh = convert_mp(mp_right)

        if lh.is_Matrix or rh.is_Matrix:
            return mat_mul_flat(lh, rh)
        else:
            return mul_flat(lh, rh)
    elif mp.DIV() or mp.CMD_DIV() or mp.COLON():
        lh = convert_mp(mp_left)
        rh = convert_mp(mp_right)
        if lh.is_Matrix or rh.is_Matrix:
            return sympy.MatMul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
        else:
            return sympy.Mul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
    elif mp.CMD_MOD():
        lh = convert_mp(mp_left)
        rh = convert_mp(mp_right)
        if rh.is_Matrix:
            raise Exception("Cannot perform modulo operation with a matrix as an operand")
        else:
            return sympy.Mod(lh, rh, evaluate=False)
    else:
        if hasattr(mp, 'unary'):
            return convert_unary(mp.unary())
        else:
            return convert_unary(mp.unary_nofunc())


def convert_unary(unary):
    if hasattr(unary, 'unary'):
        nested_unary = unary.unary()
    else:
        nested_unary = unary.unary_nofunc()
    if hasattr(unary, 'postfix_nofunc'):
        first = unary.postfix()
        tail = unary.postfix_nofunc()
        postfix = [first] + tail
    else:
        postfix = unary.postfix()

    if unary.ADD():
        return convert_unary(nested_unary)
    elif unary.SUB():
        tmp_convert_nested_unary = convert_unary(nested_unary)
        if tmp_convert_nested_unary.is_Matrix:
            return mat_mul_flat(-1, tmp_convert_nested_unary, evaluate=False)
        else:
            if tmp_convert_nested_unary.func.is_Number:
                return -tmp_convert_nested_unary
            else:
                return mul_flat(-1, tmp_convert_nested_unary)
    elif postfix:
        return convert_postfix_list(postfix)


def convert_postfix_list(arr, i=0):
    if i >= len(arr):
        raise Exception("Index out of bounds")

    res = convert_postfix(arr[i])

    if isinstance(res, sympy.Expr) or isinstance(res, sympy.And) or isinstance(res, sympy.Not) or isinstance(res,
                                                                                                             sympy.Or) or isinstance(
        res,
        sympy.Matrix) or res is sympy.S.EmptySet or isinstance(
        res,
        bool) or isinstance(
        res,
        set) or isinstance(
        res,
        sympy.Set) or isinstance(res, (list, tuple)) or isinstance(res, (Zero, One, BooleanFalse, BooleanTrue)):
        if i == len(arr) - 1:
            return res  # nothing to multiply by
        else:
            # multiply by next
            rh = convert_postfix_list(arr, i + 1)

            if res.is_Matrix or rh.is_Matrix:
                return mat_mul_flat(res, rh)
            else:
                return mul_flat(res, rh)
    else:  # must be derivative
        wrt = res[0]
        if i == len(arr) - 1:
            raise Exception("Expected expression for derivative")
        else:
            expr = convert_postfix_list(arr, i + 1)
            return sympy.Derivative(expr, wrt)


def do_subs(expr, at):
    if at.expr():
        at_expr = convert_expr(at.expr())
        syms = at_expr.atoms(sympy.Symbol)
        if len(syms) == 0:
            return expr
        elif len(syms) > 0:
            sym = next(iter(syms))
            return expr.subs(sym, at_expr)
    elif at.equality():
        lh = convert_expr(at.equality().expr(0))
        rh = convert_expr(at.equality().expr(1))
        return expr.subs(lh, rh)


def convert_postfix(postfix):
    if hasattr(postfix, 'exp'):
        exp_nested = postfix.exp()
    else:
        exp_nested = postfix.exp_nofunc()

    exp = convert_exp(exp_nested)
    for op in postfix.postfix_op():
        if op.BANG():
            if isinstance(exp, list):
                raise Exception("Cannot apply postfix to derivative")
            exp = sympy.factorial(exp, evaluate=False)
        elif op.eval_at():
            ev = op.eval_at()
            at_b = None
            at_a = None
            if ev.eval_at_sup():
                at_b = do_subs(exp, ev.eval_at_sup())
            if ev.eval_at_sub():
                at_a = do_subs(exp, ev.eval_at_sub())
            if at_b is not None and at_a is not None:
                exp = add_flat(at_b, mul_flat(at_a, -1))
            elif at_b is not None:
                exp = at_b
            elif at_a is not None:
                exp = at_a

    return exp


def convert_exp(exp):
    if hasattr(exp, 'exp'):
        exp_nested = exp.exp()
    else:
        exp_nested = exp.exp_nofunc()

    if exp_nested:
        base = convert_exp(exp_nested)
        if isinstance(base, list):
            raise Exception("Cannot raise derivative to power")
        if exp.atom():
            exponent = convert_atom(exp.atom())
        elif exp.expr():
            exponent = convert_expr(exp.expr())
        return sympy.Pow(base, exponent, evaluate=False)
    else:
        if hasattr(exp, 'comp'):
            return convert_comp(exp.comp())
        else:
            return convert_comp(exp.comp_nofunc())


def convert_comp(comp):
    if comp.group():
        return convert_expr(comp.group().expr())
    elif comp.abs_group():
        return sympy.Abs(convert_expr(comp.abs_group().expr()), evaluate=False)
    elif comp.floor_group():
        return handle_floor(convert_expr(comp.floor_group().expr()))
    elif comp.ceil_group():
        return handle_ceil(convert_expr(comp.ceil_group().expr()))
    elif comp.atom():
        return convert_atom(comp.atom())
    elif comp.frac():
        return convert_frac(comp.frac())
    elif comp.binom():
        return convert_binom(comp.binom())
    elif comp.matrix():
        return convert_matrix(comp.matrix())
    elif comp.func():
        return convert_func(comp.func())


def convert_atom(atom):
    if atom.LETTER_NO_E():
        subscriptName = ''
        s = atom.LETTER_NO_E().getText()
        if s == "I":
            return sympy.I
        if atom.subexpr():
            subscript = None
            if atom.subexpr().expr():  # subscript is expr
                subscript = convert_expr(atom.subexpr().expr())
            else:  # subscript is atom
                subscript = convert_atom(atom.subexpr().atom())
            subscriptName = '_{' + StrPrinter().doprint(subscript) + '}'
        return sympy.Symbol(atom.LETTER_NO_E().getText() + subscriptName, real=True)
    elif atom.GREEK_LETTER():
        s = atom.GREEK_LETTER().getText()[1:]
        if atom.subexpr():
            subscript = None
            if atom.subexpr().expr():  # subscript is expr
                subscript = convert_expr(atom.subexpr().expr())
            else:  # subscript is atom
                subscript = convert_atom(atom.subexpr().atom())
            subscriptName = StrPrinter().doprint(subscript)
            s += '_{' + subscriptName + '}'
        return sympy.Symbol(s, real=True)
    elif atom.accent():
        # get name for accent
        name = atom.accent().start.text[1:]
        # exception: check if bar or overline which are treated both as bar
        if name in ["bar", "overline"]:
            name = "bar"
        # get the base (variable)
        base = atom.accent().base.getText()
        # set string to base+name
        s = base + name
        if atom.subexpr():
            subscript = None
            if atom.subexpr().expr():  # subscript is expr
                subscript = convert_expr(atom.subexpr().expr())
            else:  # subscript is atom
                subscript = convert_atom(atom.subexpr().atom())
            subscriptName = StrPrinter().doprint(subscript)
            s += '_{' + subscriptName + '}'
        return sympy.Symbol(s, real=True)
    elif atom.SYMBOL():
        s = atom.SYMBOL().getText().replace("\\$", "").replace("\\%", "")
        if s == "\\infty":
            return sympy.oo
        elif s == '\\pi':
            return sympy.pi
        elif s == '\\emptyset':
            return sympy.S.EmptySet
        else:
            raise Exception("Unrecognized symbol")
    elif atom.NUMBER():
        s = atom.NUMBER().getText().replace(",", "")
        try:
            sr = sympy.Rational(s)
            return sr
        except (TypeError, ValueError):
            return sympy.Number(s)
    elif atom.E_NOTATION():
        s = atom.E_NOTATION().getText().replace(",", "")
        try:
            sr = sympy.Rational(s)
            return sr
        except (TypeError, ValueError):
            return sympy.Number(s)
    elif atom.DIFFERENTIAL():
        var = get_differential_var(atom.DIFFERENTIAL())
        return sympy.Symbol('d' + var.name, real=True)
    elif atom.mathit():
        text = rule2text(atom.mathit().mathit_text())
        return sympy.Symbol(text, real=True)
    elif atom.VARIABLE():
        text = atom.VARIABLE().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        name = text[10:]
        name = name[0:len(name) - trim_amount]
        symbol_name = name
        dimension = None
        if "_" in name:
            variables = name.split('_')
            variable, dimension = variables[0], "_".join(variables[1:])
            dimension = dimension[1: len(dimension) - 1]
            dimension = process_sympy(dimension)
            symbol_name = variable
            print("Variable", variable, ", Dimension", dimension)
        # add hash to distinguish from regular symbols
        # hash = hashlib.md5(name.encode()).hexdigest()
        # symbol_name = name + hash

        # replace the variable for already known variable values
        if name in VARIABLE_VALUES:
            # if a sympy class
            if isinstance(VARIABLE_VALUES[name], tuple(sympy.core.all_classes)):
                symbol = VARIABLE_VALUES[name]

            # if NOT a sympy class
            else:
                symbol = parse_expr(str(VARIABLE_VALUES[name]))
        else:
            symbol = sympy.Symbol(symbol_name, real=True)

        if is_percent:
            return sympy.Mul(symbol, sympy.Pow(100, -1, evaluate=False), evaluate=False)

        if dimension:
            symbolname = StrPrinter().doprint(dimension)
            return sympy.Symbol(symbol_name + "(" + symbolname + ")")
        return symbol


    elif atom.EQUALITY_CMD():
        s = atom.EQUALITY_CMD().getText()
        if '<' in s:
            blank = atom.EQUALITY_CMD().getText().split('<')
            return sympy.StrictLessThan(process_sympy(blank[0]), process_sympy(blank[1]))
        elif '>' in s:
            blank = atom.EQUALITY_CMD().getText().split('>')
            return sympy.StrictGreaterThan(process_sympy(blank[0]), process_sympy(blank[1]))
        elif '\\leq' in s:
            blank = atom.EQUALITY_CMD().getText().split('\\leq')
            return sympy.LessThan(process_sympy(blank[0]), process_sympy(blank[1]))
        elif '\\geq' in s:
            blank = atom.EQUALITY_CMD().getText().split('\\geq')
            return sympy.GreaterThan(process_sympy(blank[0]), process_sympy(blank[1]))
        elif '=' in s:
            blank = atom.EQUALITY_CMD().getText().split('=')
            return sympy.Eq(process_sympy(blank[0]), process_sympy(blank[1]))
        elif '\\neq' in s:
            blank = atom.EQUALITY_CMD().getText().split('\\neq')
            return sympy.Ne(process_sympy(blank[0]), process_sympy(blank[1]))
        else:
            raise Exception("Unrecognized symbol")


    elif atom.FOR_CMD():
        s = atom.FOR_CMD().getText().split('\\for')
        s = process_sympy(s[0]), process_sympy(s[1])
        return list(s)

    elif atom.LEN_CMD():
        text = atom.LEN_CMD().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        name = text[5:]
        name = name[0:len(name) - trim_amount]
        name = process_sympy(name,variable_values=VARIABLE_VALUES)
        return name


    elif atom.SET_CMD():
        s = atom.SET_CMD().getText()
        if '\\cup' in s:
            temps = s.split('\\cup')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)

            def cus_union(lis1, lis2):
                res = set().union(lis1, lis2)
                return res

            for i in blank[1:]:
                a = cus_union(blank[0], i)
                blank[0] = a
            symbol = blank[0]
            return symbol
        elif '\\cap' in s:
            temps = s.split('\\cap')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)

            def cus_intersection(lis1, lis2):
                res = set().intersection(lis1, lis2)
                return res

            for i in blank[1:]:
                a = cus_intersection(blank[0], i)
                blank[0] = a
            symbol = blank[0]
            return symbol
        elif '\\subseteq' in s:
            temps = s.split('\\subseteq')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)
            symbol_subset = (blank[0]).issubset(blank[1])
            return symbol_subset

        elif '\\supseteq' in s:
            temps = s.split('\\supseteq')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)
            symbol_subset = (blank[0]).issuperset(blank[1])
            return symbol_subset

        elif '\\subset' in s:
            temps = s.split('\\subset')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)
            symbol_subset = (blank[0]).issubset(blank[1])
            if symbol_subset == True and blank[0] < blank[1]:
                return True
            return False

        elif '\\supset' in s:
            temps = s.split('\\supset')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)
            symbol_subset = (blank[0]).issuperset(blank[1])
            if symbol_subset == True and blank[0] > blank[1]:
                return True
            return False

        elif '\\in' in s:
            temps = s.split('\\in')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)
            if list(blank[0])[0] in blank[1]:
                symbol = True
                return symbol
            return False

        elif '\\notin' in s:
            temps = s.split('\\notin')
            blank = []
            for temp in temps:
                val = set(map(str, set(process_sympy(temp).name)))
                blank.append(val)
            if list(blank[0])[0] not in blank[1]:
                symbol = True
                return symbol
            return False

        else:
            raise Exception("Unrecognized symbol")

    elif atom.INTERVAL():
        t = atom.INTERVAL().getText()
        if '[' in t and ']' in t:
            s = atom.INTERVAL().getText().split('\\in')
            s = sympy.Interval(process_sympy(s[1])[0], process_sympy(s[1])[1]).contains(process_sympy(s[0]))
            return s
        elif '[' in t and '>' in t:
            s = atom.INTERVAL().getText().split('\\in')
            s1 = s[1].replace('>', ']')
            s = sympy.Interval.Ropen(process_sympy(s1)[0], process_sympy(s1)[1]).contains(process_sympy(s[0]))
            return s
        elif '<' in t and '>' in t:
            s = atom.INTERVAL().getText().split('\\in')
            s1 = s[1].replace('>', ']')
            s1 = s1.replace('<', '[')
            s = sympy.Interval.open(process_sympy(s1)[0], process_sympy(s1)[1]).contains(process_sympy(s[0]))
            return s

        elif '<' in t and ']' in t:
            s = atom.INTERVAL().getText().split('\\in')
            s1 = s[1].replace('<', '[')
            s = sympy.Interval.Lopen(process_sympy(s1)[0], process_sympy(s1)[1]).contains(process_sympy(s[0]))
            return s

    elif atom.SUMMATION():
        text = atom.SUMMATION().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        name = text[5:]

        name = name[0:len(name) - trim_amount]
        # add hash to distinguish from regular symbols
        # hash = hashlib.md5(name.encode()).hexdigest()
        # symbol_name = name + hash
        symbol_name = name

        if name in VARIABLE_VALUES:
            # if a sympy class
            if isinstance(VARIABLE_VALUES[name], tuple(sympy.core.all_classes)):
                symbol = VARIABLE_VALUES[name]

            # if NOT a sympy class
            else:
                symbol = parse_expr(str(VARIABLE_VALUES[name]))
        else:
            symbol = process_sympy(symbol_name)
            a, b, c, d = symbol[0], symbol[1], symbol[2], symbol[3]
            symbol = sympy.summation(a, (b, c, d))

        return symbol

    elif atom.EQUIVALENCE():
        text = atom.EQUIVALENCE().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        name = text[13:]

        name = name[0:len(name) - trim_amount]
        # add hash to distinguish from regular symbols
        # hash = hashlib.md5(name.encode()).hexdigest()
        # symbol_name = name + hash
        symbol_name = name

        # replace the variable for already known variable values
        if name in VARIABLE_VALUES:
            # if a sympy class
            if isinstance(VARIABLE_VALUES[name], tuple(sympy.core.all_classes)):
                symbol = VARIABLE_VALUES[name]

            # if NOT a sympy class
            else:
                symbol = parse_expr(str(VARIABLE_VALUES[name]))
        else:
            symbol = process_sympy(symbol_name)
            a, b = symbol[0], symbol[1]
            symbol = sympy.Equivalent(a, b)

        # return the symbol
        return symbol

    elif atom.NRT():
        text = atom.NRT().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        name = text[5:]
        name = name[0:len(name) - trim_amount]
        symbol_name = name

        # replace the variable for already known variable values
        if name in VARIABLE_VALUES:
            # if a sympy class
            if isinstance(VARIABLE_VALUES[name], tuple(sympy.core.all_classes)):
                symbol = VARIABLE_VALUES[name]

            # if NOT a sympy class
            else:
                symbol = parse_expr(str(VARIABLE_VALUES[name]))
        else:
            symbol = process_sympy(symbol_name)
            symbol = sympy.Pow(symbol[0], 1 / symbol[1])

            # symbol = list(map(list, [symbol[0].name, symbol[1].name]))

        if is_percent:
            return sympy.Mul(symbol, sympy.Pow(100, -1, evaluate=False), evaluate=False)

        # return the symbol
        return symbol

    elif atom.CONDITIONAL():
        text = atom.CONDITIONAL().getText()



    elif atom.LOGICAL():
        text = atom.LOGICAL().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        if "\\land" in text[:6]:
            name = text[6:]
        elif "\\neg" in text[:5]:
            name = text[5:]
        elif "\\lor" in text[:5]:
            name = text[5:]
        name = name[0:len(name) - trim_amount]
        symbol_name = name

        # replace the variable for already known variable values
        if name in VARIABLE_VALUES:
            # if a sympy class
            if isinstance(VARIABLE_VALUES[name], tuple(sympy.core.all_classes)):
                symbol = VARIABLE_VALUES[name]

            # if NOT a sympy class
            else:
                symbol = parse_expr(str(VARIABLE_VALUES[name]))
        else:
            symbol = process_sympy(symbol_name)
            if "land" in text[:6]:
                symbol = And(symbol[0], symbol[1])
            elif "lor" in text[:5]:
                symbol = sympy.Or(symbol[0], symbol[1])
            else:
                symbol = Not(symbol)

            # symbol = list(map(list, [symbol[0].name, symbol[1].name]))

        if is_percent:
            return sympy.Mul(symbol, sympy.Pow(100, -1, evaluate=False), evaluate=False)

        # return the symbol
        return symbol

    elif atom.SET_EQUALITY():
        text = atom.SET_EQUALITY().getText()
        is_percent = text.endswith("\\%")
        trim_amount = 3 if is_percent else 1
        name = text[10:]
        name = name[0:len(name) - trim_amount]
        print(name)
        symbol_name = name
        symbol = process_sympy(symbol_name)
        return sympy.Equality(symbol[0], symbol[1])

    elif atom.ABSOLUTE():
        text = atom.ABSOLUTE().getText().split('\\absolute')
        text = sympy.Abs(process_sympy(text[1]))
        return text


    elif atom.PERCENT_NUMBER():
        s = atom.PERCENT_NUMBER().getText()
        if '\\%' in s:
            text = atom.PERCENT_NUMBER().getText().replace("\\%", "").replace(",", "")
            try:
                number = sympy.Rational(text)
            except (TypeError, ValueError):
                number = sympy.Number(text)
            percent = sympy.Rational(number, 100)
            return percent
        elif '\\‰' in s:
            text = atom.PERCENT_NUMBER().getText().replace("\\‰", "").replace(",", "")
            try:
                number = sympy.Rational(text)
            except (TypeError, ValueError):
                number = sympy.Number(text)
            percent = sympy.Rational(number, 1000)
            return percent
        elif '\\per_thousand' in s:
            text = atom.PERCENT_NUMBER().getText().replace("\\per_thousand", "").replace(",", "")
            try:
                number = sympy.Rational(text)
            except (TypeError, ValueError):
                number = sympy.Number(text)
            percent = sympy.Rational(number, 1000)
            return percent


def rule2text(ctx):
    stream = ctx.start.getInputStream()
    # starting index of starting token
    startIdx = ctx.start.start
    # stopping index of stopping token
    stopIdx = ctx.stop.stop

    return stream.getText(startIdx, stopIdx)


def convert_frac(frac):
    diff_op = False
    partial_op = False
    lower_itv = frac.lower.getSourceInterval()
    lower_itv_len = lower_itv[1] - lower_itv[0] + 1
    if (frac.lower.start == frac.lower.stop and
            frac.lower.start.type == PSLexer.DIFFERENTIAL):
        wrt = get_differential_var_str(frac.lower.start.text)
        diff_op = True
    elif (lower_itv_len == 2 and
          frac.lower.start.type == PSLexer.SYMBOL and
          frac.lower.start.text == '\\partial' and
          (frac.lower.stop.type == PSLexer.LETTER_NO_E or frac.lower.stop.type == PSLexer.SYMBOL)):
        partial_op = True
        wrt = frac.lower.stop.text
        if frac.lower.stop.type == PSLexer.SYMBOL:
            wrt = wrt[1:]

    if diff_op or partial_op:
        wrt = sympy.Symbol(wrt, real=True)
        if (diff_op and frac.upper.start == frac.upper.stop and
                frac.upper.start.type == PSLexer.LETTER_NO_E and
                frac.upper.start.text == 'd'):
            return [wrt]
        elif (partial_op and frac.upper.start == frac.upper.stop and
              frac.upper.start.type == PSLexer.SYMBOL and
              frac.upper.start.text == '\\partial'):
            return [wrt]
        upper_text = rule2text(frac.upper)

        expr_top = None
        if diff_op and upper_text.startswith('d'):
            expr_top = process_sympy(upper_text[1:])
        elif partial_op and frac.upper.start.text == '\\partial':
            expr_top = process_sympy(upper_text[len('\\partial'):])
        if expr_top:
            return sympy.Derivative(expr_top, wrt)

    expr_top = convert_expr(frac.upper)
    expr_bot = convert_expr(frac.lower)
    if expr_top.is_Matrix or expr_bot.is_Matrix:
        return sympy.MatMul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)
    else:
        return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)


def convert_binom(binom):
    expr_top = convert_expr(binom.upper)
    expr_bot = convert_expr(binom.lower)
    return sympy.binomial(expr_top, expr_bot)


def convert_func(func):
    if func.func_normal_single_arg():
        if func.L_PAREN():  # function called with parenthesis
            arg = convert_func_arg(func.func_single_arg())
        else:
            arg = convert_func_arg(func.func_single_arg_noparens())

        name = func.func_normal_single_arg().start.text[1:]

        # change arc<trig> -> a<trig>
        if name in ["arcsin", "arccos", "arctan", "arccsc", "arcsec",
                    "arccot"]:
            name = "a" + name[3:]
            expr = getattr(sympy.functions, name)(arg, evaluate=False)
        elif name in ["arsinh", "arcosh", "artanh"]:
            name = "a" + name[2:]
            expr = getattr(sympy.functions, name)(arg, evaluate=False)
        elif name in ["arcsinh", "arccosh", "arctanh"]:
            name = "a" + name[3:]
            expr = getattr(sympy.functions, name)(arg, evaluate=False)
        elif name == "operatorname":
            operatorname = func.func_normal_single_arg().func_operator_name.getText()

            if operatorname in ["arsinh", "arcosh", "artanh"]:
                operatorname = "a" + operatorname[2:]
                expr = getattr(sympy.functions, operatorname)(arg, evaluate=False)
            elif operatorname in ["arcsinh", "arccosh", "arctanh"]:
                operatorname = "a" + operatorname[3:]
                expr = getattr(sympy.functions, operatorname)(arg, evaluate=False)
            elif operatorname == "floor":
                expr = handle_floor(arg)
            elif operatorname == "ceil":
                expr = handle_ceil(arg)
        elif name in ["log", "ln"]:
            if func.subexpr():
                if func.subexpr().atom():
                    base = convert_atom(func.subexpr().atom())
                else:
                    base = convert_expr(func.subexpr().expr())
            elif name == "log":
                base = 10
            elif name == "ln":
                base = sympy.E
            expr = sympy.log(arg, base, evaluate=False)
        elif name in ["exp", "exponentialE"]:
            expr = sympy.exp(arg)
        elif name == "floor":
            expr = handle_floor(arg)
        elif name == "ceil":
            expr = handle_ceil(arg)

        func_pow = None
        should_pow = True
        if func.supexpr():
            if func.supexpr().expr():
                func_pow = convert_expr(func.supexpr().expr())
            else:
                func_pow = convert_atom(func.supexpr().atom())

        if name in ["sin", "cos", "tan", "csc", "sec", "cot", "sinh", "cosh", "tanh"]:
            if func_pow == -1:
                name = "a" + name
                should_pow = False
            expr = getattr(sympy.functions, name)(arg, evaluate=False)

        if func_pow and should_pow:
            expr = sympy.Pow(expr, func_pow, evaluate=False)

        return expr

    elif func.func_normal_multi_arg():
        if func.L_PAREN():  # function called with parenthesis
            args = func.func_multi_arg().getText().split(",")
        else:
            args = func.func_multi_arg_noparens().split(",")

        args = list(map(lambda arg: process_sympy(arg, VARIABLE_VALUES), args))
        name = func.func_normal_multi_arg().start.text[1:]

        if name == "operatorname":
            operatorname = func.func_normal_multi_arg().func_operator_name.getText()
            if operatorname in ["gcd", "lcm"]:
                expr = handle_gcd_lcm(operatorname, args)
        elif name in ["gcd", "lcm"]:
            expr = handle_gcd_lcm(name, args)
        elif name in ["max", "min"]:
            name = name[0].upper() + name[1:]
            expr = getattr(sympy.functions, name)(*args, evaluate=False)

        func_pow = None
        should_pow = True
        if func.supexpr():
            if func.supexpr().expr():
                func_pow = convert_expr(func.supexpr().expr())
            else:
                func_pow = convert_atom(func.supexpr().atom())

        if func_pow and should_pow:
            expr = sympy.Pow(expr, func_pow, evaluate=False)

        return expr

    # elif func.LETTER_NO_E() or func.SYMBOL():
    #     print('LETTER_NO_E or symbol')
    #     if func.LETTER_NO_E():
    #         fname = func.LETTER_NO_E().getText()
    #     elif func.SYMBOL():
    #         fname = func.SYMBOL().getText()[1:]
    #     fname = str(fname) # can't be unicode
    #     if func.subexpr():
    #         subscript = None
    #         if func.subexpr().expr():                   # subscript is expr
    #             subscript = convert_expr(func.subexpr().expr())
    #         else:                                       # subscript is atom
    #             subscript = convert_atom(func.subexpr().atom())
    #         subscriptName = StrPrinter().doprint(subscript)
    #         fname += '_{' + subscriptName + '}'
    #     input_args = func.args()
    #     output_args = []
    #     while input_args.args():                        # handle multiple arguments to function
    #         output_args.append(convert_expr(input_args.expr()))
    #         input_args = input_args.args()
    #     output_args.append(convert_expr(input_args.expr()))
    #     return sympy.Function(fname)(*output_args)

    elif func.FUNC_INT():
        return handle_integral(func)
    elif func.FUNC_SQRT():
        expr = convert_expr(func.base)
        if func.root:
            r = convert_expr(func.root)
            return sympy.Pow(expr, 1 / r, evaluate=False)
        else:
            return sympy.Pow(expr, sympy.S.Half, evaluate=False)
    elif func.FUNC_SUM():
        return handle_sum_or_prod(func, "summation")
    elif func.FUNC_PROD():
        return handle_sum_or_prod(func, "product")
    elif func.FUNC_LIM():
        return handle_limit(func)
    elif func.EXP_E():
        return handle_exp(func)


def convert_func_arg(arg):
    if hasattr(arg, 'expr'):
        return convert_expr(arg.expr())
    else:
        return convert_mp(arg.mp_nofunc())


def handle_integral(func):
    if func.additive():
        integrand = convert_add(func.additive())
    elif func.frac():
        integrand = convert_frac(func.frac())
    else:
        integrand = 1

    int_var = None
    if func.DIFFERENTIAL():
        int_var = get_differential_var(func.DIFFERENTIAL())
    else:
        for sym in integrand.atoms(sympy.Symbol):
            s = str(sym)
            if len(s) > 1 and s[0] == 'd':
                if s[1] == '\\':
                    int_var = sympy.Symbol(s[2:], real=True)
                else:
                    int_var = sympy.Symbol(s[1:], real=True)
                int_sym = sym
        if int_var:
            integrand = integrand.subs(int_sym, 1)
        else:
            # Assume dx by default
            int_var = sympy.Symbol('x', real=True)

    if func.subexpr():
        if func.subexpr().atom():
            lower = convert_atom(func.subexpr().atom())
        else:
            lower = convert_expr(func.subexpr().expr())
        if func.supexpr().atom():
            upper = convert_atom(func.supexpr().atom())
        else:
            upper = convert_expr(func.supexpr().expr())
        return sympy.Integral(integrand, (int_var, lower, upper))
    else:
        return sympy.Integral(integrand, int_var)


def handle_sum_or_prod(func, name):
    val = convert_mp(func.mp())
    iter_var = convert_expr(func.subeq().equality().expr(0))
    start = convert_expr(func.subeq().equality().expr(1))
    if func.supexpr().expr():  # ^{expr}
        end = convert_expr(func.supexpr().expr())
    else:  # ^atom
        end = convert_atom(func.supexpr().atom())

    if name == "summation":
        return sympy.Sum(val, (iter_var, start, end))
    elif name == "product":
        return sympy.Product(val, (iter_var, start, end))


def handle_limit(func):
    sub = func.limit_sub()
    if sub.LETTER_NO_E():
        var = sympy.Symbol(sub.LETTER_NO_E().getText(), real=True)
    elif sub.GREEK_LETTER():
        var = sympy.Symbol(sub.GREEK_LETTER().getText()[1:], real=True)
    else:
        var = sympy.Symbol('x', real=True)
    if sub.SUB():
        direction = "-"
    else:
        direction = "+"
    approaching = convert_expr(sub.expr())
    content = convert_mp(func.mp())

    return sympy.Limit(content, var, approaching, direction)


def handle_exp(func):
    if func.supexpr():
        if func.supexpr().expr():  # ^{expr}
            exp_arg = convert_expr(func.supexpr().expr())
        else:  # ^atom
            exp_arg = convert_atom(func.supexpr().atom())
    else:
        exp_arg = 1
    return sympy.exp(exp_arg)


def handle_gcd_lcm(f, args):
    """
    Return the result of gcd() or lcm(), as UnevaluatedExpr

    f: str - name of function ("gcd" or "lcm")
    args: List[Expr] - list of function arguments
    """

    args = tuple(map(sympy.nsimplify, args))

    # gcd() and lcm() don't support evaluate=False
    return sympy.UnevaluatedExpr(getattr(sympy, f)(args))


def handle_floor(expr):
    """
    Apply floor() then return the floored expression.

    expr: Expr - sympy expression as an argument to floor()
    """
    return sympy.functions.floor(expr, evaluate=False)


def handle_ceil(expr):
    """
    Apply ceil() then return the ceil-ed expression.

    expr: Expr - sympy expression as an argument to ceil()
    """
    return sympy.functions.ceiling(expr, evaluate=False)


def get_differential_var(d):
    text = get_differential_var_str(d.getText())
    return sympy.Symbol(text, real=True)


def get_differential_var_str(text):
    for i in range(1, len(text)):
        c = text[i]
        if not (c == " " or c == "\r" or c == "\n" or c == "\t"):
            idx = i
            break
    text = text[idx:]
    if text[0] == "\\":
        text = text[1:]
    return text
