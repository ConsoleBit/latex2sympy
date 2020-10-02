from sympy import Symbol, Equality

import latex2sympy


a = r"1+2-3\cdot\frac{4}{5}+6^7+\sqrt{5}+6+\variable{DEMO_{abc,bca,cde}}"
b = latex2sympy.process_sympy(a)
print(b)

# for i in b.free_symbols:
#     if "_" in i.name:
#         variable, dimension = i.name.split('_')
#         dimension = dimension[1: len(dimension) - 1]
#         dimension = dimension.split(",")
#         print("Variable", variable, ", Dimension", dimension)
# print(b.evalf(1))

#
# fragment UNION_SYMBOL: L_PAREN  (DIGIT | COMMA | LETTER)+ R_PAREN COMMA L_PAREN (DIGIT | COMMA | LETTER)+ R_PAREN;
# UNION : UNION_CMD L_BRACE (VARIABLE | COMMA | DIGIT)+ R_BRACE;
#
# fragment INTERSECTION_SYMBOL: L_PAREN  (DIGIT | COMMA | LETTER)+ R_PAREN COMMA L_PAREN (DIGIT | COMMA | LETTER)+ R_PAREN;
# INTERSECTION : INTERSECTION_CMD L_BRACE (VARIABLE | COMMA)+ R_BRACE;
#
# fragment  PROPER_SUBSET_SYMBOL: L_PAREN  (DIGIT | COMMA | LETTER)+ R_PAREN COMMA L_PAREN (DIGIT | COMMA | LETTER)+ R_PAREN;
# PROPER_SUBSET : PROPER_SUBSET_CMD L_BRACE (VARIABLE | COMMA)+ R_BRACE;