from interpreter import eval_expression

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
