#!/usr/bin/env python2
import sys
from parser import parse
from interpreter import interpret

globalScope = {}
while True:
    code = raw_input("> ")
    if code == "quit" or code == "q" or code == "die":
        break
    try:
        ast = parse(code)
        try:
            interpret(ast)
        except:
            e = sys.exc_info()[0]
            print "Error interpreting:",e
    except:
        e = sys.exc_info()[0]
        print "Error parsing:",e
