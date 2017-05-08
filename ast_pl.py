"""
Abstract Syntax Tree (AST) for propositional logic sentences
author: Michael Grupp
"""

import itertools as it


# constant and variable nodes for AST
class Const:
    value = False

    def __init__(self, value):
        self.value = value


class Var:
    name = ''
    value = False

    def __init__(self, name, value=False):
        self.value = value
        self.name = name


# expression types for AST
class Expr:
    # this class only defines the basic expression interface
    # all real expression types inherit/override it
    opName = ''  # operator name
    # an expression has its arguments as children
    # children can be Const, Var or Expr
    children = []

    def __init__(self, child1=None, child2=None):
        self.children = [child1, child2]

    def add_child(self, child):
        self.children.append(child)

    def basic_op(self, arg_vals):
        # the basic operation, override this for every Expr type
        return None

    def calc(self):
        # recursively calculate the expression and its children
        arg_vals = []
        for child in self.children:
            if isinstance(child, Expr):
                arg_vals.append(child.calc())
            elif isinstance(child, Var) or isinstance(child, Const):
                arg_vals.append(child.value)
        return self.basic_op(arg_vals)


class Sentence(Expr):
    # start of an AST, only one child
    opName = 'Sentence'

    def __init__(self, child):
        self.children = [child]


class NOT(Expr):
    # a negation expression
    opName = '~'

    def __init__(self, child=None):  # not can have only one child
        self.children = [child]

    def basic_op(self, arg_vals):
        return not arg_vals[0]


class OR(Expr):
    # an or expression
    opName = 'or'

    def basic_op(self, arg_vals):
        return arg_vals[0] or arg_vals[1]


class AND(Expr):
    # an and expression
    opName = 'and'

    def basic_op(self, arg_vals):
        return arg_vals[0] and arg_vals[1]


class IMPL(Expr):
    # an implication expression
    opName = '==>'

    def basic_op(self, arg_vals):
        return (not arg_vals[0]) or arg_vals[1]  # implication elimination


class BIDI(Expr):
    # a bidirectional expression
    opName = '<=>'

    def basic_op(self, arg_vals):
        # biconditional and implication elimination
        return ((not arg_vals[0]) or arg_vals[1]) and ((not arg_vals[1]) or arg_vals[0])


class AST:
    # Abstract Syntax Tree - representation of a sentence's syntax
    # the AST is a tree of Expr, Var and Const nodes
    startNode = None
    varValueDict = dict()  # dictionary: 'Var.name' --> Var.value

    def __init__(self, start_node):
        self.startNode = start_node

    def print_sentence(self, node):
        # traverse AST recursively and print it
        for child in node.children:
            if isinstance(child, Expr):
                print((child.opName + '('), end=' ')
                self.print_sentence(child)
                print(')', end=' ')
            elif isinstance(child, Var):
                print(child.name, end=' ')
            elif isinstance(child, Const):
                print(str(child.value), end=' ')

    def init_dict(self, node):
        # traverse AST recursively and initialize the varValueDict
        for child in node.children:
            if isinstance(child, Expr):
                self.init_dict(child)
            elif isinstance(child, Var):
                if child.name not in self.varValueDict:
                    self.varValueDict[child.name] = child.value

    def calc_sentence(self):
        # calculate the output of the sentence with current variable values
        res = (self.startNode.children[0].calc())
        return res

    def assign_current_values(self, node):
        # assign current values from dictionary varValueDict to variables in AST
        for child in node.children:
            if isinstance(child, Expr):
                self.assign_current_values(child)
            elif isinstance(child, Var):
                child.value = self.varValueDict[child.name]

    def evaluate_all_models(self):
        # test all possible models - return list of all results
        self.init_dict(self.startNode)
        res = []
        var_count = len(self.varValueDict)
        all_models = it.product([True, False], repeat=var_count)  # cartesian product
        for model in all_models:
            for key, i in zip(self.varValueDict, list(range(var_count))):
                # import the values from all_models to varValueDict
                self.varValueDict[key] = model[i]
            self.assign_current_values(self.startNode)
            res.append(self.calc_sentence())
        return res

    # the actual theorem checks
    def valid(self):
        # true in all models
        results = self.evaluate_all_models()
        if False in results:
            return False
        else:
            return True

    def satisfiable(self):
        # true in one or more models
        results = self.evaluate_all_models()
        if True in results:
            return True
        else:
            return False

    def unsatisfiable(self):
        # false in all models
        results = self.evaluate_all_models()
        if True not in results:
            return True
        else:
            return False

    def entails(self, other_ast):
        # theorem 3.1 from sheet: a entails b if and(a not(b)) is unsatisfiable
        a = AND(self.startNode.children[0], NOT(other_ast.startNode.children[0]))
        s = Sentence(a)  # conjunction and(a not(b))
        entailed = AST(s)  # temporal AST
        return entailed.unsatisfiable()
