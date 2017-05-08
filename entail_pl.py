"""
Check if a propositional logic sentence entails another sentence
Specify the two sentences below and run this file to see the result.

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

sentence_a = 'A <=> B'  # entails...
sentence_b = '~A \/ B'

parser = pp.Parser()
tokenList_a = parser.lex(sentence_a)
tokenList_b = parser.lex(sentence_b)
ast_a = parser.parse(tokenList_a)
ast_b = parser.parse(tokenList_b)

print('1st sentence:', end=' ')
ast_a.print_sentence(ast_a.startNode)
print('\n2nd sentence:', end=' ')
ast_b.print_sentence(ast_b.startNode)

print('\n1st sentence entails 2nd sentence: ' + str(ast_a.entails(ast_b)))
