def read_token(code):
    code = code.strip()

    if code[0] == "(":
        # Token is a list
        remaining = code[1:]
        tokens = []

        while len(remaining) > 0 and remaining[0] != ")":
            token, remaining = read_token(remaining)
            tokens.append(token)
            remaining = remaining.lstrip()

        if len(remaining) > 0 and remaining[0] == ")":
            remaining = remaining[1:].lstrip()

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

def unparse(code):
    if isinstance(code, list):
        val = "("
        for i in code:
            if isinstance(i, list):
                val += unparse(i)
            else:
                val += "%s " % str(i)

        return val + ")"

    else:
        return str(code)
