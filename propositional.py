# -*- coding: utf-8 -*-
"""
Created on Sun Jan 03 15:03:22 2016

@author: Michael
"""

import re
import itertools as it

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

#expression types for AST
class Expr:
    #this class only defines the basic expression interface
    #all real expression types inherit/override it
    opName = '' #operator name
    #an expression has its arguments as children
    #children can be Const, Var or Expr    
    children = []
    def __init__(self, child1=None, child2=None):
        self.children = [child1, child2]
    def addChild(self, child):
        self.children.append(child)
    def basicOp(self, argVals):
        #the basic operation, override this for every Expr type
        return None
    def calc(self):
        #recursively calculate the expression and its children
        argVals = []
        for child in self.children:
            if isinstance(child, Expr):
                argVals.append(child.calc())
            elif isinstance(child, Var) or isinstance(child, Const):
                argVals.append(child.value)
        return self.basicOp(argVals)

class Sentence(Expr):
    #start of an AST, only one child
    opName = 'Sentence'
    def __init__(self, child):
        self.children = [child]

class NOT(Expr):
    #a negation expression
    opName = '~'
    def __init__(self, child=None): #not can have only one child
        self.children = [child]
    def basicOp(self, argVals):
        return not argVals[0]

class OR(Expr):
    #an or expression
    opName = 'or'
    def basicOp(self, argVals):
        return argVals[0] or argVals[1]

class AND(Expr):
    #an and expression
    opName = 'and'
    def basicOp(self, argVals):
        return argVals[0] and argVals[1]   
    
class IMPL(Expr):
    #an implication expression
    opName = '==>'
    def basicOp(self, argVals):
        return (not argVals[0]) or argVals[1] #implication elimination

class BIDI(Expr):
    #a bidirectional expression
    opName = '<=>'
    def basicOp(self, argVals):
        #biconditional and implication elimination
        return ((not argVals[0]) or argVals[1]) and ((not argVals[1]) or argVals[0])

class AST:
    #Abstract Syntax Tree - representation of a sentence's syntax
    #the AST is a tree of Expr, Var and Const nodes
    startNode = None
    varValueDict = dict() #dictionary: 'Var.name' --> Var.value
    
    def __init__(self, startNode):
        self.startNode = startNode
    
    def toString(self, node):
        #traverse AST recursively and print it
        for child in node.children:
            if isinstance(child, Expr):
                print (child.opName + '('), #comma supresses newline
                self.toString(child)
                print (')'),
            elif isinstance(child, Var):
                print (child.name),# + '[' + str(child.value) +']'),
            elif isinstance(child, Const):
                print str(child.value),

    def countVariables(self, node, count):
        #traverse AST recursively and count unique variables
        #initializes the varValueDict
        #(in and(a a), a is only counted once)
        for child in node.children:
            if isinstance(child, Expr):
                count = self.countVariables(child, count)
            elif isinstance(child, Var):
                if child.name not in self.varValueDict:                    
                    self.varValueDict[child.name] = child.value
                    count += 1
        return count
        
    def calcSentence(self):
        #calculate the output of the sentence with current variable values
        res = []
        #for child in self.startNode.children:
        res.append(self.startNode.children[0].calc())
        return res
    
    def assignCurrentValues(self, node):
        #assign current values from dictionary varValueDict to variables in AST
        for child in node.children:
            if isinstance(child, Expr):
                self.assignCurrentValues(child)
            elif isinstance(child, Var):
                child.value = self.varValueDict[child.name]
    
    def evaluateAllModels(self, node, res):
        #test all possible models - return list of all results
        varCount = len(self.varValueDict)
        allModels = it.product([True,False],repeat=varCount) #cartesian product
        for model in allModels: 
            for key, i in zip(self.varValueDict, range(varCount)):
                #import the values from allModels to varValueDict
                self.varValueDict[key] = model[i]
            self.assignCurrentValues(self.startNode)
            res.append(self.calcSentence())
        return res
        
class PropLogic:
    def __init__(self):
        pass    
    def valid(formula):
        #true in all models
        pass
    def satisfiable(formula):
        #true in one or more models
        pass
    def unsatisfiable(formula):
        #false in all models
        pass
    def entails(formula1, formula2):
        #theorem 3.1 from sheet: a entails b if and(a not(b)) is unsatisfiable
        pass
    
#key tokens in propositional logic
operators = ['<=>', '==>', 'or', 'and', '~']
constants = ['true', 'false']

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
        return list(filter(None, re.split('(==>|<=>|and|or|~|[()])', string)))
    
    #temporal containers used during parsing
    groups = [] #expressions in ( )
    const = [] #constants
    var = [] #variables
    negs = [] #predicates (negation in propositional logic)
    structure = [] #the currently parsed syntax structure (quite similar to AST)
    previous = 'none' #previously parsed token    
    
    def addExprToStructure(self, expr, token):
        if self.previous == 'var':
            expr.addChild(self.var.pop())
        elif self.previous in constants:
            expr.addChild(self.const.pop())
        elif self.previous == ')':
            expr.addChild(self.groups.pop())
        self.structure.append(expr)
        self.previous = token
    
    def addConstToStructure(self, val, token):
        if self.previous == '~': 
            self.const.append(NOT(Const(val)))
            self.negs.pop()
        else:
            self.const.append(Const(val))
        if self.previous in operators and self.previous != '~':
            self.structure[-1].addChild(self.const.pop())        
        self.previous = token
    
    def parse(self, tokenList):
        #parse a token list and generate an AST
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
                    self.groups.append(NOT(self.structure.pop()))
                else:
                    self.groups.append(self.structure.pop())
                if argumentGroup:
                    self.structure[-1].addChild(self.groups.pop())
                self.previous = token
            elif token == '~':
                #nots are the only operators that can be children of operators
                #expr = NOT()
                #self.structure.append(expr)
                self.negs.append(NOT())
                self.previous = token
            elif token == 'and':
                expr = AND()
                self.addExprToStructure(expr, token)
            elif token == 'or':
                expr = OR()
                self.addExprToStructure(expr, token)
            elif token == '==>':
                expr = IMPL()
                self.addExprToStructure(expr, token)
            elif token == '<=>':
                expr = BIDI()
                self.addExprToStructure(expr, token)
            elif token == 'true':
                self.addConstToStructure(True, token)
            elif token == 'false':
                self.addConstToStructure(False, token)
            else :
                #variable      
                if self.previous == '~': 
                    self.var.append(NOT(Var(token)))
                    self.negs.pop()
                else:
                    self.var.append(Var(token))
                if self.previous in operators and self.previous != '~':
                    self.structure[-1].addChild(self.var.pop()) 
                self.previous = 'var'
        if self.groups and not self.structure:
           #if sentence consists only of a group...
            self.structure.append(self.groups.pop())
        elif self.groups:
            #if there is a group left that was not yet appended to structure...
            self.structure[-1].addChild(self.groups.pop())
        #return the AST object of this parsing session
        return AST(Sentence(self.structure.pop()))


################
# main program 
# usage: avoid brackets, double negations
parser = Parser();
string = 'a \/ b'

tokenList = parser.lex(string)

ast = parser.parse(tokenList)
ast.toString(ast.startNode)
print 'variable count: ' + str(ast.countVariables(ast.startNode, 0))

res = []
ast.evaluateAllModels(ast.startNode, res)
print res
pass