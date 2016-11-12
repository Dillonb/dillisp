#!/usr/bin/env python2
from parser import parse
from interpreter import interpret

globalScope = {}
while True:
    code = raw_input("> ")
    if code == "quit" or code == "q" or code == "die":
        break

    ast = parse(code)
    interpret(ast)
