#!/usr/bin/env python
import sys
import re
import readline
open('/tmp/.lisp_history', "a+").close()
HISTORY_FILENAME = '/tmp/.lisp_history'
readline.read_history_file(HISTORY_FILENAME)
readline.parse_and_bind('tab: complete')


def format(code):
    s = ""
    if type(code) is str:
        return code

    for k, x in enumerate(code):
        if x == '(' or x == ')':
            s += x
        elif k < len(code)-1 and code[k+1] != ')':
            s += (x+' ' if type(x) is str else format(x) + ' ')
        else:
            s += x
    return s


def extractMatchBracket(tokens):
    if not tokens or tokens[0] != '(':
        return None
    stack = []
    left = right = 0
    while not left or (left and left != right):
        stack.append(tokens.pop(0))
        if stack[-1] == '(':
            left += 1
        if stack[-1] == ')':
            right += 1

    return stack


def extractAllMatchBracket(tokens):
    t = list(tokens)
    bs = []
    while True:
        tmp = extractMatchBracket(t)
        if not tmp:
            break
        bs.append(tmp)
    if t:
        raise SyntaxError("bracket not match")
    return bs


def extractAllexpr(tokens):
    t = list(tokens)
    bs = []

    while True:
        if not t:
            break
        if t[0] == '(':
            bs.append(extractMatchBracket(t))
        else:
            bs.append(t[0])
            t.pop(0)
    if t:
        raise SyntaxError("bracket not match")
    return bs


def isLegalList(tokens):
    return True if extractAllMatchBracket(tokens)else False


def isAtom(tokens):
    if len(tokens) == 1:
        token = tokens[0]
        atom = re.compile(r'^[a-zA-z_][a-zA-z0-9_]*\??$')
        if len(atom.findall(token)) >= 0:
            return 't'
    return 'nil'


def evaluate(expression):
    expression.pop(0)
    expression.pop()

    try:
        return symbols[expression[0]](expression[1:])
    except KeyError:
        raise SyntaxError("symbol %s is not callable" % expression[0])


def parse(tokens):
    if len(tokens) > 1:
        expression = extractMatchBracket(tokens)
        if expression:
            return evaluate(expression)
        return None
    return tokens[0]


def quote(args):
    # r = extractAllMatchBracket(args)
    r = extractAllexpr(args)

    if len(r) > 1:
        raise SyntaxError("too many argument for quote")
    return r[0]


def car(args):
    r = extractAllMatchBracket(args)
    if len(r) > 1:
        raise SyntaxError("too many argument for car")
    r = r[0]
    if isAtom(r) == 't':
        raise SyntaxError("argument should be list")

    res = parse(r)

    return extractMatchBracket(res[1:-1]) if res[1] == '(' else res[1]


def cdr(args):
    r = extractAllMatchBracket(args)
    if len(r) > 1:
        raise SyntaxError("too many argument for cdr")
    r = r[0]
    if isAtom(r) == 't':
        raise SyntaxError("argument should be list")

    res = parse(r)[1:-1]

    exprs = extractAllexpr(res)
    if len(exprs) < 2:
        return 'nil'
    # raise NotImplementedError

    return ['('] + exprs[1:] + [')']


def cons(args):
    r = [parse(x) for x in extractAllexpr(args)]

    if len(r) != 2:
        raise SyntaxError("cons require two arguments")

    if isAtom(r[1]) == 't':
        raise SyntaxError("the second argument must be a list")

    return [r[1][0]] + [r[0]] + r[1][1:]


def cond(args):
    r = extractAllexpr(args)
    for x in r:
        if isAtom(x) == 't' or len(extractAllexpr(x)) != 2:
            raise SyntaxError("arguments must be list of length two")

    for x in r:
        cond, expr = extractAllexpr(x)
        res = parse(cond)
        if res != 'nil' and res != ['(', ')']:
            return parse(expr)

    return 'nil'


symbols = {
    'quote': quote,
    'atom': isAtom,
    'eq': lambda x: 't' if parse(x) == parse(x) else 'nil',
    'car': car,
    'cdr': cdr,
    'cons': cons,
    'cond': cond,
}


def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def interpret(s):
    return format(parse(tokenize(s)))


if __name__ == "__main__":
    print "winkar's lisp interpreter"
    while True:
        try:
            s = raw_input('>')
            print interpret(s)
        except EOFError:
            print '\nbye'
            sys.exit(0)
        except SyntaxError, e:
            print e
            continue
        except Exception, e:
            print e
            import traceback
            traceback.print_exc()
        finally:
            readline.write_history_file(HISTORY_FILENAME)
