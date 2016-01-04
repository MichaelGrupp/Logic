# -*- coding: utf-8 -*-
"""
Created on Sun Jan 03 15:03:22 2016

@author: Michael
"""

import re

"""
logical operators in Python:
AND OR NOT
True False
"""

#operators in propositional logic, descending order
operators = ['(', ')', '<=>', '==>', 'or', 'and', '~']
constants = ['true', 'false']

#constant and variable nodes for AST
class Const:
    value = False;
    def __init__(self, value):
        self.value = value

class Var:
    name = ''
    value = False
    def __init__(self, name, value=False):
        self.value = value
        self.name = name

#expression nodes for AST
class Expr:
    opName = '' #operator name, for easier printing later
    #an expression has its arguments as children
    #children can be Const, Var or Expr    
    children = []
    def __init__(self, child1, child2):
        self.children = [child1, child2]
    def addChild(self, child):
        self.children = child

class Sentence(Expr):
    opName = 'Sentence'
    def __init__(self, child): #start of an AST, only one child
        self.children = [child]

class NOT(Expr):
    opName = '~'
    def __init__(self, child): #not can have only one child
        self.children = [child]
    
class OR(Expr):
    opName = 'or'

class AND(Expr):
    opName = 'and'

class IMPL(Expr):
    opName = '==>'

class BIDI(Expr):
    opName = '<=>'

class AST:
    #the AST is a tree of Expr, Var and Const nodes
    startNode = None
    
    def traverse(self, node):
        for child in node.children:
            if isinstance(child, Expr):
                print (child.opName + '('), #comma supresses newline
                self.traverse(child)
                print (')'),
            elif isinstance(child, Var):
                print (child.name),# + '[' + str(child.value) +']'),
            elif isinstance(child, Const):
                print (child.value),
class Formula:
    bids = [] #'<=>' bidirectional expressions    
    imps = [] #'==>' implication expressions
    ors = [] #'or' expressions
    ands = [] #'and' expressions
    nots = [] #'~' not expressions
    
    def __init__(self):
        pass

class PropLogic:
    def __init__(self):
        pass    
    def valid(formula):
        pass
    def satisfiable(formula):
        pass
    def unsatisfiable(formula):
        pass
    def entails(formula):
        pass
    
    
class Parser:
    badPatterns = [' ', '/\\', '\\/'] #critical patterns to be replaced in clean step
    goodPatterns = ['', 'and', 'or'] #patterns used as replacement in clean step
    
    def __init__(self):
        pass

    def clean(self, string):
        #patterns containing backslashes are critical in python (escape symbol)
        #replace such patterns defined in badPatterns by those in goodPatterns
        for old, new in zip(self.badPatterns, self.goodPatterns):
            string = string.replace(old, new)
        return string
    
    def lex(self, string):
        #split a space delimited string 
        #in a list of unordered tokens (operator, keys, symbols)
        #e.g. 'a /\ b' --> ['a', 'and', 'b']
        string = self.clean(string)        
        return list(filter(None, re.split('(and|or|~|[()])', string)))
    
    def parse(tokenList):
        for token in tokenList:
            if token == '(':
                pass
            elif token == ')':
                pass
            elif token == '~':
                pass
            elif token == 'and':
                pass
            elif token == 'or':
                pass
            elif token == '==>':
                pass
            elif token == '<=>':
                pass
            elif token == 'true':
                pass
            elif token == 'false':
                pass
            else :
                #variable
                pass

#def main():
parser = Parser();
string = '(alpha) ==> ~gamma'
symbolList = parser.lex(string)
print string
print symbolList

expr1 = OR(Var('alpha'), Var('beta', True))
expr2 = AND(Var('gamma'), NOT(Var('omega')))
expr3 = IMPL(expr1, expr2)
expr = Sentence(expr3)

ast = AST()
ast.startNode = expr
ast.traverse(ast.startNode)
pass