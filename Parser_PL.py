# -*- coding: utf-8 -*-
"""
Parser for propositional logic sentences written in ASCII syntax

Created on Tue Jan 05 18:56:47 2016

@author: Michael
"""

import re
import AST_PL as ap

#key tokens in propositional logic
operators = ['<=>', '==>', 'or', 'and', '~']
constants = ['true', 'false']

class Parser:
    badPatterns = [' ', '/\\', '\\/'] #critical patterns to be replaced in clean step
    goodPatterns = ['', 'and', 'or'] #patterns used as replacement in clean step
    
    #temporal containers used during parsing
    groups = [] #expressions in ( )
    const = [] #constants
    var = [] #variables
    negs = [] #predicates (negation in propositional logic)
    structure = [] #the currently parsed syntax structure (quite similar to AST)
    previous = 'none' #previously parsed token    
    
    def __init__(self):
        pass
    
    def reset(self):
        self.groups = []
        self.const = []
        self.var = []
        self.negs = []
        self.structure = []
        self.previous = 'none'    
    
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
        return list(filter(None, re.split('(==>|<=>|and|or|~|[()])', string)))
    
    def addExprToStructure(self, expr, token):
        if self.previous == 'var' and self.var:
            #var stack is empty at 2nd operator in chained expression: a /\ b \/ c
            expr.addChild(self.var.pop())
        elif self.previous in constants and self.const:
            expr.addChild(self.const.pop())
        elif self.previous == ')' and self.groups:
            #group stack is empty at 3rd operator in chain: A \/ (B /\ C) /\ D
            expr.addChild(self.groups.pop())
        else:
            expr.addChild(self.structure.pop()) #chained expression: a /\ b \/ c
        self.structure.append(expr)
        self.previous = token
    
    def addConstToStructure(self, val, token):
        if self.previous == '~' or self.previous == '(~': 
            self.const.append(ap.NOT(ap.Const(val)))
            self.negs.pop()
        else:
            self.const.append(ap.Const(val))
        if self.previous in operators and self.previous not in ['(~'] and self.structure: #TODO: hack to avoid '~a /\ (~b /\ ~c) ' crash... better solution?
            self.structure[-1].addChild(self.const.pop()) 
        self.previous = token
    
    def parse(self, tokenList):
        #parse a token list and generate an AST
        self.reset()
        argumentGroup = False
        for token in tokenList:
            if token == '(':
                if self.previous in operators and self.previous != '~':
                    argumentGroup = True
                else:
                    argumentGroup = False
                self.previous = token
            elif token == ')':
                if self.negs: #if negation predicate exists...
                    self.negs.pop()
                    self.groups.append(ap.NOT(self.structure.pop()))
                else:
                    self.groups.append(self.structure.pop())
                if argumentGroup:
                    self.structure[-1].addChild(self.groups.pop())
                self.previous = token
            elif token == '~':
                #nots are the only operators that can be children of operators
                self.negs.append(ap.NOT())
                if self.previous == '(': 
                    self.previous = '(~' #TODO: hack to avoid 'a /\ (~b /\ ~c) ' crash... better solution?
                else:
                    self.previous = token
            elif token == 'and':
                expr = ap.AND()
                self.addExprToStructure(expr, token)
            elif token == 'or':
                expr = ap.OR()
                self.addExprToStructure(expr, token)
            elif token == '==>':
                expr = ap.IMPL()
                self.addExprToStructure(expr, token)
            elif token == '<=>':
                expr = ap.BIDI()
                self.addExprToStructure(expr, token)
            elif token == 'true':
                self.addConstToStructure(True, token)
            elif token == 'false':
                self.addConstToStructure(False, token)
            else :
                #variable      
                if self.previous == '~' or self.previous == '(~': 
                    self.var.append(ap.NOT(ap.Var(token)))
                    self.negs.pop()
                else:
                    self.var.append(ap.Var(token))
                if self.previous in operators and self.previous not in ['(~'] and self.structure: #TODO: hack to avoid '~a /\ (~b /\ ~c) ' crash... better solution?
                    self.structure[-1].addChild(self.var.pop()) 
                self.previous = 'var'
        if self.groups and not self.structure:
           #if sentence consists only of a group...
            self.structure.append(self.groups.pop())
        elif self.groups:
            #if there is a group left that was not yet appended to structure...
            self.structure[-1].addChild(self.groups.pop())
        elif self.const:
            #if sentence contains only a constant
            self.structure.append(self.const.pop())
        elif self.var:
            #if sentence contains only a variable
            self.structure.append(self.var.pop())
        #return the AST object of this parsing session
        return ap.AST(ap.Sentence(self.structure.pop()))
