#!/usr/bin/env python2
import sys
from parser import parse
from interpreter import Interpreter
import traceback

interpreter = Interpreter()

def dump_error(exc):
    e, value, tb = exc

    print e
    print value
    for line in traceback.format_tb(tb):
        print line

if len(sys.argv) < 2:
    print "Usage: %s <script>"%sys.argv[0]
else:
    code = open(sys.argv[1]).read()
    try:
        ast = parse(code)
        try:
            interpreter.silent_interpret(ast)
        except:
            print "Error interpreting"
            dump_error(sys.exc_info())
    except:
        print "Error parsing"
        dump_error(sys.exc_info())

