# -*- coding: utf-8 -*-
"""
Created on Sun Jan 03 15:03:22 2016

@author: Michael
"""

import re #regex

"""
logical operators in Python:
AND OR NOT
True False
"""
class Formula:
    atoms = []
    

class PropLogic:
    def valid(formula):
        pass
    
    def satisfiable(formula):
        pass
    
    def unsatisfiable(formula):
        pass
    
    def entails(formula):
        pass
    
    
class Parser:
    badPatterns = ["/\\", "\\/"] #critical patterns to be replaced in clean step
    goodPatterns = ['and', 'or'] #patterns used as replacement in clean step
    
    #operators in propositional logic, descending order
    operators = ['<=>', '==>', 'or', 'and', '~']
    keys = ['true', 'false']
    
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
        return re.split(',', string)
    
    def parse(tokenList):
        #convert the token list into a formula        
        pass
    
    
#def main():
    parser = Parser();
    string = '(a /\ ~b)'
    symbolList = parser.lex(string)
    print string
    print symbolList
    pass