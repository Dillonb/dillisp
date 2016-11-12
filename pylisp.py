def read_token(code):
    code = code.strip()

    if code[0] == "(":
        # Token is a list
        remaining = code[1:]
        tokens = []

        while len(remaining) > 0 and remaining[0] != ")":
            token, remaining = read_token(remaining)
            tokens.append(token)

            remaining = remaining[1:]

        return tokens, remaining
    elif code[0] == "\"":
        pass # TODO: token is a String
    else:
        remaining = code
        token = ""

        while len(remaining) > 0 and remaining[0] != " " and remaining[0] != ")":
            token += remaining[0]
            remaining = remaining[1:]

        try:
            temp = int(token)
            return temp, remaining
        except ValueError:
            try:
                temp = float(token)
                return temp, remaining
            except ValueError:
                return token, remaining

def parse(code):
    """Tokenizes a code string, parses and returns an AST"""
    tokens = []
    remaining = code

    while True:
        token, remaining = read_token(remaining)
        tokens.append(token)
        if remaining == "":
            return tokens

def do_print(vals):
    print(" ".join(vals))

stdlib = {
    '*': lambda args: reduce(lambda a,b: a*b, args),
    '/': lambda args: reduce(lambda a,b: a/b, args),
    '+': lambda args: reduce(lambda a,b: a+b, args),
    '-': lambda args: reduce(lambda a,b: a-b, args),
    'print': lambda args: do_print(args),
    'input': lambda args: apply(input, args)
}

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

def interpret(ast):
    """Interprets an AST"""
    globalScope = {}
    for expression in ast:
        print eval_expression(expression, globalScope)



ast = parse("(* 2 (+ 1 2))")

interpret(ast)
