# -*- coding: utf-8 -*-
"""
Check if a propositional logic sentence entails another sentence

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

Created on Tue Jan 05 19:57:53 2016

@author: Michael
"""

import Parser_PL as pp
import AST_PL as ap

sentence_a = 'A <=> B'
sentence_b = '~A \/ B'

parser = pp.Parser();
tokenList_a = parser.lex(sentence_a)
tokenList_b = parser.lex(sentence_b)
ast_a = parser.parse(tokenList_a)
ast_b = parser.parse(tokenList_b)

print '1st sentence: ', 
ast_a.printSentence(ast_a.startNode)
print '\n2nd sentence: ', 
ast_b.printSentence(ast_b.startNode)

print '\n1st sentence entails 2nd sentence: ' + str(ast_a.entails(ast_b))