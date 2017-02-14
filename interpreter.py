from parser import parse, unparse

import math
import numbers
import sys
from itertools import izip_longest

consts = {
    'None': None,
    'pi': math.pi,
    'True': True,
    'true': True,
    'False': False,
    'false': False
}

builtins = {
    '*': lambda args, parentScope: reduce(lambda a,b: a*b, eval_arguments(args, parentScope)),
    '/': lambda args, parentScope: reduce(lambda a,b: a/b, eval_arguments(args, parentScope)),
    '+': lambda args, parentScope: reduce(lambda a,b: a+b, eval_arguments(args, parentScope)),
    '-': lambda args, parentScope: reduce(lambda a,b: a-b, eval_arguments(args, parentScope)),
    '**': lambda args, parentScope: reduce(lambda a,b: a**b, eval_arguments(args, parentScope)),
    '%': lambda args, parentScope: reduce(lambda a,b: a%b, eval_arguments(args, parentScope)),
    '>': lambda args, parentScope: greater_than(args, parentScope),
    '<': lambda args, parentScope: less_than(args, parentScope),
    '=': lambda args, parentScope: reduce(lambda a,b: a==b, eval_arguments(args, parentScope)),
    'print': lambda args, parentScope: do_print(eval_arguments(args, parentScope)),
    'input': lambda args, parentScope: apply(input, eval_arguments(args, parentScope)),
    'lambda': lambda args, parentScope: Function(args[0], args[1], parentScope),
    'tailcall-lambda': lambda args, parentScope: TailCallFunction(args[0], args[1], args[2], parentScope),
    'incomplete-tailcall': lambda args, parentScope: IncompleteTailCallRecursion(eval_arguments(args, parentScope)),
    'define': lambda args, parentScope: do_define(args, parentScope),
    'if': lambda args, parentScope: do_if(args, parentScope),
    'and': lambda args, parentScope: reduce(lambda a,b: a and b, eval_arguments(args, parentScope)),
    'or': lambda args, parentScope: reduce(lambda a,b: a or b, eval_arguments(args, parentScope)),
    'not': lambda args, parentScope: not eval_arguments(args, parentScope)[0],
    'head': lambda args, parentScope: eval_arguments(args, parentScope)[0][0],
    'tail': lambda args, parentScope: eval_arguments(args, parentScope)[0][1:],
    'last': lambda args, parentScope: eval_arguments(args, parentScope)[0][-1],
    'map': lambda args, parentScope: do_map(args, parentScope),
    'reduce': lambda args, parentScope: do_reduce(args, parentScope),
    'filter': lambda args, parentScope: do_filter(args, parentScope),
    'defn': lambda args, parentScope: do_defn(args, parentScope, forceTailCall=False),
    'taildefn': lambda args, parentScope: do_defn(args, parentScope, forceTailCall=True),
    'append': lambda args, parentScope: do_append(eval_arguments(args, parentScope), parentScope),
    'none?': lambda args, parentScope: eval_arguments(args, parentScope)[0] == None
}

def do_append(args, parentScope):
    return args[0] + (args[1],)


def do_map(args, parentScope):
    func = eval_expression(args[0], parentScope)
    l = eval_expression(args[1], parentScope)
    result = []
    for item in l:
        result.append(func.eval([item], parentScope))
    return tuple(result)

def do_filter(args, parentScope):
    func = eval_expression(args[0], parentScope)
    l = eval_expression(args[1], parentScope)
    result = []
    for item in l:

        if func.eval([item], parentScope):
            result.append(item)

    return tuple(result)

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
    def __init__(self, argList, expr, parentScope):
        if isinstance(argList, list):
            self.argList = argList
        else:
            self.argList = [argList]
        self.expr = expr
        self.parentScope = parentScope

    def eval(self, args, callingScope):
        scope = {}
        scope['__parent__'] = self.parentScope

        args = map(lambda arg: eval_expression(arg, callingScope), args)

        extra = []

        for name, val in izip_longest(self.argList, args):
            if name is not None:
                scope[name] = val
            else:
                extra.append(val)

        scope['...'] = tuple(extra)

        return eval_expression(self.expr, scope)

    def __str__(self):
        return "(lambda %s %s)" % (unparse(self.argList), unparse(self.expr) )

class IncompleteTailCallRecursion(Function):
    def __init__(self, argList):
        self.argList = argList

    def __str__(self):
        return '('+ ' '.join(map(lambda x: str(x), self.argList)) + ')'

def replace_call_with(code, orig, replacement):
    if isinstance(code, list) and len(code) > 0:
        new = replacement if code[0] == orig else code[0]
        return [new] + map(lambda x: replace_call_with(x, orig, replacement), code[1:])
    return code

class TailCallFunction:
    def __init__(self, name, argList, expr, parentScope):
        # Replace all recursive calls with calls to a special function that tells us we're not done - incomplete-tailcall
        self.origCode = expr
        self.code = replace_call_with(expr, name, 'incomplete-tailcall')
        self.func = Function(argList, self.code, parentScope)

    def eval(self, args, callingScope):
        result = self.func.eval(args, callingScope)

        while isinstance(result, IncompleteTailCallRecursion):
            result = self.func.eval(result.argList, callingScope)

        return result

    def __str__(self):
        return "(lambda %s %s)" % (unparse(self.func.argList), unparse(self.origCode))

def do_define(args, parentScope):
    if len(args) != 2:
        raise Exception("Invalid syntax on define call")

    if args[0] in builtins or args[0] == "__parent__":
        raise Exception("Invalid name! Must not conflict with built-ins or equal __parent__")

    parentScope[args[0]] = eval_expression(args[1], parentScope)

    return eval_expression(args[1], parentScope)

def function_in_code(nameOfFunction, code):
    if isinstance(code, list) and len(code) > 0:
        return code[0] == nameOfFunction or (len(code) > 1 and reduce(lambda a,b: a or b, map(lambda x: function_in_code(nameOfFunction, x), code[1:])))
    return False

def can_tail_call(name, code):
    if isinstance(code, list) and len(code) > 0:
        if (code[0] == "if"):
            # Recurse down through ifs
            return can_tail_call(name, code[2]) and can_tail_call(name, code[3])
        else:
            # If this is a call to our function, and there are no recursive calls within the arguments
            if code[0] == name:
                for expr in code[1:]:
                    if function_in_code(name, expr):
                        return False
                return True
            else:
                return False
    return True # This is just an expression, we can return

def do_defn(args, parentScope, forceTailCall):
    should_tailcall = function_in_code(args[0], args[2])
    can_tailcall = should_tailcall and can_tail_call(args[0], args[2])

    if (forceTailCall):
        if not can_tailcall:
            raise Exception("Function cannot be tail call optimized")

    if can_tailcall:
        code = [args[0], ['tailcall-lambda' if can_tailcall else 'lambda', args[0], args[1], args[2]]]
    else:
        code = [args[0], ['lambda', args[1], args[2]]]

    return do_define(code, parentScope)

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
        if isinstance(expression, tuple) or isinstance(expression, numbers.Number) or isinstance(expression, Function) or isinstance(expression, TailCallFunction):
            result = expression
        elif expression[0] == '\'':
            result = expression[1:]
        elif expression in consts:
            result = consts[expression]
        elif expression in builtins:
            result = "builtin"
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
            result = eval_expression(expression, self.globalScope)
            if result is not None:
                print(result)

    def interpret_and_return(self, ast):
        return map(lambda expr: eval_expression(expr, self.globalScope), ast)
