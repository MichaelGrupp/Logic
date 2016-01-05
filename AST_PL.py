# -*- coding: utf-8 -*-
"""
Abstract Syntax Tree (AST) for propositional logic sentences

Created on Tue Jan 05 18:53:09 2016

@author: Michael
"""

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
    
    def printSentence(self, node):
        #traverse AST recursively and print it
        for child in node.children:
            if isinstance(child, Expr):
                print (child.opName + '('), #comma supresses newline
                self.printSentence(child)
                print (')'),
            elif isinstance(child, Var):
                print (child.name),# + '[' + str(child.value) +']'),
            elif isinstance(child, Const):
                print str(child.value),

    def initDict(self, node):
        #traverse AST recursively and initialize the varValueDict
        for child in node.children:
            if isinstance(child, Expr):
                self.initDict(child)
            elif isinstance(child, Var):
                if child.name not in self.varValueDict:                    
                    self.varValueDict[child.name] = child.value
        
    def calcSentence(self):
        #calculate the output of the sentence with current variable values
        res = (self.startNode.children[0].calc())
        return res
    
    def assignCurrentValues(self, node):
        #assign current values from dictionary varValueDict to variables in AST
        for child in node.children:
            if isinstance(child, Expr):
                self.assignCurrentValues(child)
            elif isinstance(child, Var):
                child.value = self.varValueDict[child.name]
    
    def evaluateAllModels(self, node):
        #test all possible models - return list of all results
        self.initDict(self.startNode)
        res = []
        varCount = len(self.varValueDict)
        allModels = it.product([True,False],repeat=varCount) #cartesian product
        for model in allModels: 
            for key, i in zip(self.varValueDict, range(varCount)):
                #import the values from allModels to varValueDict
                self.varValueDict[key] = model[i]
            self.assignCurrentValues(self.startNode)
            res.append(self.calcSentence())
        return res
    
    #the actual theorem checks
    def valid(self):
        #true in all models
        results = self.evaluateAllModels(self.startNode)
        if False in results:
            return False
        else:
            return True
            
    def satisfiable(self):
        #true in one or more models
        results = self.evaluateAllModels(self.startNode)
        if True in results:
            return True
        else:
            return False
            
    def unsatisfiable(self):
        #false in all models
        results = self.evaluateAllModels(self.startNode)
        if True not in results:
            return True
        else:
            return False
            
    def entails(self, otherAST):
        #theorem 3.1 from sheet: a entails b if and(a not(b)) is unsatisfiable
        a = AND(self.startNode.children[0], NOT(otherAST.startNode.children[0]))
        s = Sentence(a)  #conjunction and(a not(b))
        entailed = AST(s) #temporal AST
        return entailed.unsatisfiable() 