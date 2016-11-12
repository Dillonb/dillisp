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

while True:
    code = raw_input("> ")
    if code == "quit" or code == "q" or code == "die":
        break
    try:
        ast = parse(code)
        try:
            interpreter.interpret(ast)
        except:
            print "Error interpreting"
            dump_error(sys.exc_info())
    except:
        print "Error parsing"
        dump_error(sys.exc_info())
