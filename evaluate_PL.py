# -*- coding: utf-8 -*-
"""
Evaluate sentences in propositional logic
Enter your sentence below and run this file to see the result in the output.

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

Created on Sun Jan 03 15:03:22 2016

@author: Michael
"""

import Parser_PL as pp
import AST_PL as ap

sentence = '(Fire ==> Smoke) /\ Fire /\ ~Smoke'

parser = pp.Parser();
tokenList = parser.lex(sentence)
ast = parser.parse(tokenList)

ast.printSentence(ast.startNode)

print '\nis valid (tautology): ' + str(ast.valid())
print 'is satisfiable: ' + str(ast.satisfiable())
print 'is unsatisfiable: ' + str(ast.unsatisfiable())