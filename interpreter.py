stdlib = {
    '*': lambda args, parentScope: reduce(lambda a,b: a*b, eval_arguments(args, parentScope)),
    '/': lambda args, parentScope: reduce(lambda a,b: a/b, eval_arguments(args, parentScope)),
    '+': lambda args, parentScope: reduce(lambda a,b: a+b, eval_arguments(args, parentScope)),
    '-': lambda args, parentScope: reduce(lambda a,b: a-b, eval_arguments(args, parentScope)),
    '>': lambda args, parentScope: greater_than(args, parentScope),
    '<': lambda args, parentScope: less_than(args, parentScope),
    '=': lambda args, parentScope: reduce(lambda a,b: a==b, eval_arguments(args, parentScope)),
    'print': lambda args, parentScope: do_print(eval_arguments(args, parentScope)),
    'input': lambda args, parentScope: apply(input, eval_arguments(args, parentScope)),
    'lambda': lambda args, parentScope: do_lambda(args),
    'define': lambda args, parentScope: do_define(args, parentScope),
    'if': lambda args, parentScope: do_if(args, parentScope)
}

def do_if(args, parentScope):
    if eval_expression(args[0]):
        return args[1]
    else:
        return args[2]

def greater_than(args, parentScope):
    last = float('inf')
    for val in args:
        val = eval_expression(val)
        if not last > val:
            return False
        last = val
    return True

def less_than(args, parentScope):
    last = float('-inf')
    for val in args:
        val = eval_expression(val)
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

        for name, val in zip(self.argList, args):
            scope[name] = val

        return eval_expression(self.expr, scope)

def do_lambda(args):
    return Function(args[0], args[1])

def do_define(args, parentScope):
    if len(args) != 2:
        raise Exception("Invalid syntax on define call")

    if args[0] in stdlib or args[0] == "__parent__":
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
    if func in stdlib:
        return stdlib[func](args, parentScope)
    else:
        from_scope = get_from_scope(func, parentScope)
        if from_scope is not None:
            return from_scope.eval(args, parentScope)

def eval_expression(expression, scope = {}):
    if isinstance(expression, list):
        result = eval_function(expression[0], expression[1:], scope)
    else:
        from_scope = get_from_scope(expression, scope)
        if from_scope is None:
            result = expression
        else:
            result = from_scope

    return result

def interpret(ast, globalScope={}):
    """Interprets an AST"""
    for expression in ast:
        print eval_expression(expression, globalScope)
