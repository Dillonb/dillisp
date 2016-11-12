stdlib = {
    '*': lambda args: reduce(lambda a,b: a*b, args),
    '/': lambda args: reduce(lambda a,b: a/b, args),
    '+': lambda args: reduce(lambda a,b: a+b, args),
    '-': lambda args: reduce(lambda a,b: a-b, args),
    'print': lambda args: do_print(args),
    'input': lambda args: apply(input, args)
}

def do_print(vals):
    print(" ".join(map(str, vals)))

def get_from_scope(identifier, scope):
    if identifier in scope:
        return scope[identifier]
    elif '__parent__' in scope:
        return get_from_scope(identifier, scope['__parent__'])
    else:
        return None

def eval_function(func, args, scope = {}):
    if func in stdlib:
        return stdlib[func](args)
    else:
        from_scope = get_from_scope(func, scope)
        if from_scope is not None:
            pass # TODO after I implement (defn ) and (fn ) I guess


def eval_expression(expression, parentScope = {}):
    scope = {}
    scope['__parent__'] = parentScope
    if isinstance(expression, list):
        args = map(eval_expression, expression[1:], scope)
        return eval_function(expression[0], args, scope)
    else:
        return expression

def interpret(ast, globalScope={}):
    """Interprets an AST"""
    for expression in ast:
        print eval_expression(expression, globalScope)
