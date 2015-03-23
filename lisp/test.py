#!/usr/bin/env python
import unittest
from lisp import interpret


class lispTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testQuote(self):
        self.assertEqual(interpret('(quote (a b (c d)))'), '(a b (c d))')
        self.assertEqual(interpret('(quote (1 (2 3)))'), '(1 (2 3))')
        self.assertEqual(interpret('(quote a)'), 'a')

    def testAtom(self):
        self.assertEqual(interpret('(atom ())'), 'nil')
        self.assertEqual(interpret('(atom (a (b c)))'), 'nil')
        self.assertEqual(interpret('(atom 1)'), 't')
        self.assertEqual(interpret('(atom a)'), 't')

    def testEq(self):
        self.assertEqual(interpret('(eq (atom ()) (atom ()))'), 't')
        self.assertEqual(interpret('(eq (quote (a b)) (quote (a b)))'), 't')
        self.assertEqual(interpret('(eq (atom a ) (atom ()))'), 'nil')
        self.assertEqual(interpret('(eq (quote (a c)) (quote (a b)))'), 'nil')

    def testCar(self):
        self.assertEqual(interpret('(car (quote(a b c)))'), 'a')
        self.assertEqual(interpret('(car (quote((a b) b c)))'), '(a b)')
        with self.assertRaises(SyntaxError):
            interpret('(car (a b c))')

    def testCdr(self):
        self.assertEqual(interpret('(cdr (quote (a b c)))'), '(b c)')
        self.assertEqual(interpret('(cdr (quote((a b) (b c) c)))'),
                         '((b c) c)')

    def testCons(self):
        self.assertEqual(interpret('(cons (quote (a b)) (quote (a b)))'),
                         '((a b) a b)')
        self.assertEqual(interpret('(cons (quote a) (quote (a b)))'),
                         '(a a b)')


if __name__ == "__main__":
    unittest.main()
