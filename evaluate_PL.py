# -*- coding: utf-8 -*-
"""
Evaluate sentences in propositional logic

Usage: specify sentence in ASCII syntax:
/\  : conjunction
\/  : disjunction
~   : negation
==> : implication
<=> : biconditional
( ) : brackets
constants: true false
variables: any other arbitrary string

example: (alpha /\ beta) ==> (c \/ true)

Created on Sun Jan 03 15:03:22 2016

@author: Michael
"""

import Parser_PL as pp
import AST_PL as ap

string = '(alpha /\ beta) ==> (c \/ true)'

parser = pp.Parser();
tokenList = parser.lex(string)
ast = parser.parse(tokenList)

print ast.toString(ast.startNode)

print ast.valid()
print ast.unsatisfiable()
print ast.satisfiable()
pass