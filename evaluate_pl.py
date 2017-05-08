"""
Evaluate sentences in propositional logic
Enter your sentence below and run this file to see the result.

Usage: specify sentence in ASCII syntax:
/\  : conjunction
\/  : disjunction
~   : negation
==> : implication
<=> : biconditional
( ) : brackets
constants: true false
variables: any other arbitrary string

example: (~alpha /\ beta) ==> (c \/ true)


author: Michael Grupp
"""

import parser_pl as pp

sentence = "(Fire ==> Smoke) /\ Fire /\ ~Smoke"

parser = pp.Parser()
tokenList = parser.lex(sentence)
ast = parser.parse(tokenList)

ast.print_sentence(ast.startNode)

print("\nis valid (tautology):", ast.valid())
print("is satisfiable:", ast.satisfiable())
print("is unsatisfiable:", ast.unsatisfiable())
