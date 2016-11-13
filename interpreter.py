from parser import parse
import math
import numbers
import sys

consts = {
    'None': None,
    'pi': math.pi,
    'True': True,
    'False': False
}

builtins = {
    '*': lambda args, parentScope: reduce(lambda a,b: a*b, eval_arguments(args, parentScope)),
    '/': lambda args, parentScope: reduce(lambda a,b: a/b, eval_arguments(args, parentScope)),
    '+': lambda args, parentScope: reduce(lambda a,b: a+b, eval_arguments(args, parentScope)),
    '-': lambda args, parentScope: reduce(lambda a,b: a-b, eval_arguments(args, parentScope)),
    '%': lambda args, parentScope: reduce(lambda a,b: a%b, eval_arguments(args, parentScope)),
    '>': lambda args, parentScope: greater_than(args, parentScope),
    '<': lambda args, parentScope: less_than(args, parentScope),
    '=': lambda args, parentScope: reduce(lambda a,b: a==b, eval_arguments(args, parentScope)),
    'print': lambda args, parentScope: do_print(eval_arguments(args, parentScope)),
    'input': lambda args, parentScope: apply(input, eval_arguments(args, parentScope)),
    'lambda': lambda args, parentScope: do_lambda(args),
    'memoized-lambda': lambda args, parentScope: do_memoized_lambda(args),
    'define': lambda args, parentScope: do_define(args, parentScope),
    'if': lambda args, parentScope: do_if(args, parentScope),
    'and': lambda args, parentScope: reduce(lambda a,b: a and b, eval_arguments(args, parentScope)),
    'or': lambda args, parentScope: reduce(lambda a,b: a or b, eval_arguments(args, parentScope)),
    'not': lambda args, parentScope: not eval_arguments(args, parentScope)[0],
    'list': lambda args, parentScope: eval_arguments(args, parentScope),
    'map': lambda args, parentScope: do_map(args, parentScope),
    'reduce': lambda args, parentScope: do_reduce(args, parentScope),
    'filter': lambda args, parentScope: do_filter(args, parentScope)
}

def do_map(args, parentScope):
    func = eval_expression(args[0], parentScope)
    l = eval_expression(args[1], parentScope)
    result = []
    for item in l:
        result.append(func.eval([item], parentScope))
    return result

def do_filter(args, parentScope):
    func = eval_expression(args[0], parentScope)
    l = eval_expression(args[1], parentScope)
    result = []
    for item in l:

        if func.eval([item], parentScope):
            result.append(item)

    return result

def do_reduce(args, parentScope):
    func = eval_expression(args[0], parentScope)
    l = eval_expression(args[1], parentScope)

    return reduce(lambda a,b: func.eval([a,b], parentScope), l)

def do_if(args, parentScope):
    if eval_expression(args[0], parentScope):
        return eval_expression(args[1], parentScope)
    else:
        return eval_expression(args[2], parentScope)

def greater_than(args, parentScope):
    last = float('inf')
    for val in args:
        val = eval_expression(val, parentScope)
        if not last > val:
            return False
        last = val
    return True

def less_than(args, parentScope):
    last = float('-inf')
    for val in args:
        val = eval_expression(val, parentScope)
        if not last < val:
            return False
        last = val
    return True

def eval_arguments(args, parentScope):
    newArgs = []
    for arg in args:
        newArgs.append(eval_expression(arg, parentScope))
    return newArgs

class Function:
    def __init__(self, argList, expr):
        self.argList = argList
        self.expr = expr

    def eval(self, args, parentScope):
        scope = {}
        scope['__parent__'] = parentScope

        args = map(lambda arg: eval_expression(arg, scope), args)

        for name, val in zip(self.argList, args):
            scope[name] = val

        return eval_expression(self.expr, scope)

class MemoizedFunction(Function):
    def __init__(self, argList, expr):
        Function.__init__(self, argList, expr)
        self.memoizationTable = {}

    def eval(self, args, parentScope):
        scope = {}
        scope['__parent__'] = parentScope

        args = map(lambda arg: eval_expression(arg, scope), args)

        for name, val in zip(self.argList, args):
            scope[name] = val

        if tuple(args) in self.memoizationTable:
            return self.memoizationTable[tuple(args)]

        result = eval_expression(self.expr, scope)
        self.memoizationTable[tuple(args)] = result
        return result

def do_lambda(args):
    return Function(args[0], args[1])

def do_memoized_lambda(args):
    return MemoizedFunction(args[0], args[1])

def do_define(args, parentScope):
    if len(args) != 2:
        raise Exception("Invalid syntax on define call")

    if args[0] in builtins or args[0] == "__parent__":
        raise Exception("Invalid name! Must not conflict with built-ins or equal __parent__")

    parentScope[args[0]] = eval_expression(args[1], parentScope)

    return args[1]

def do_print(vals):
    print(" ".join(map(str, vals)))

def get_from_scope(identifier, scope):
    if identifier in scope:
        return scope[identifier]
    elif '__parent__' in scope:
        return get_from_scope(identifier, scope['__parent__'])
    else:
        return None

def eval_function(func, args, parentScope = {}):
    if func in builtins:
        return builtins[func](args, parentScope)
    else:
        from_scope = get_from_scope(func, parentScope)
        if from_scope is not None:
            return from_scope.eval(args, parentScope)

def eval_expression(expression, scope):
    if isinstance(expression, list):
        result = eval_function(expression[0], expression[1:], scope)
    else:
        if isinstance(expression, numbers.Number):
            result = expression
        elif expression[0] == '\'':
            result = expression[1:]
        elif expression in consts:
            result = consts[expression]
        else:
            result = get_from_scope(expression, scope)

    return result

class Interpreter:
    def __init__(self, globalScope = {}):
        sys.setrecursionlimit(20000)
        self.globalScope = globalScope
        self.silent_interpret(parse(open("stdlib.l").read()))

    def silent_interpret(self, ast):
        for expression in ast:
            eval_expression(expression, self.globalScope)

    def interpret(self, ast):
        """Interprets an AST"""
        for expression in ast:
            print eval_expression(expression, self.globalScope)
