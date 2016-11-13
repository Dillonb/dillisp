import unittest
import random


import interpreter
import parser

def execute_code(code):
    ast = parser.parse(code)
    i = interpreter.Interpreter()
    return i.interpret_and_return(ast)[-1]

random_numbers = [(random.randint(1,1000000),random.randint(1,1000000)) for i in xrange(100)]

class ParserTest(unittest.TestCase):
    snippets = [
        [
            "(+ 1 1)",
            ['+', 1, 1]
        ],
        [
            "(+ 1 (+ 1 1))",
            ['+', 1, ['+', 1, 1]]
        ]
    ]

    def test_parser_snippets(self):
        for snippet, expected in self.snippets:
            actual = parser.parse(snippet)[0]
            self.assertEqual(actual, expected, "%s parses correctly" % snippet)

class InterpreterTest(unittest.TestCase):
    def test_add(self):
        for i,j in random_numbers:
            self.assertEqual(execute_code("(+ %d %d)"%(i,j)), i+j)
    def test_subtract(self):
        for i,j in random_numbers:
            self.assertEqual(execute_code("(- %d %d)"%(i,j)), i-j)
    def test_divide(self):
        self.assertEqual(execute_code("(/ 10 2)"), 5)
        for i,j in random_numbers:
            self.assertEqual(execute_code("(/ %d %d)"%(i,j)), i/j)
    def test_multiply(self):
        self.assertEqual(execute_code("(* 10 2)"), 20)
        for i,j in random_numbers:
            self.assertEqual(execute_code("(* %d %d)"%(i,j)), i*j)
    def test_modulus(self):
        for i,j in random_numbers:
            self.assertEqual(execute_code("(%% %d %d)"%(i,j)), i%j)
    def test_gt(self):
        for i,j in random_numbers:
            self.assertEqual(execute_code("(> %d %d)"%(i,j)), i>j)
    def test_lt(self):
        for i,j in random_numbers:
            self.assertEqual(execute_code("(< %d %d)"%(i,j)), i<j)
    def test_eq(self):
        for i,j in random_numbers:
            self.assertEqual(execute_code("(= %d %d)"%(i,j)), i==j)
    def test_lambda(self):
        pass
    def test_memoized_lambda(self):
        pass
    def test_define(self):
        pass
    def test_if(self):
        pass
    def test_and(self):
        pass
    def test_or(self):
        pass
    def test_not(self):
        pass
    def test_list(self):
        pass
    def test_map(self):
        pass
    def test_reduce(self):
        pass
    def test_filter(self):
        pass

if __name__ == '__main__':
    unittest.main()
