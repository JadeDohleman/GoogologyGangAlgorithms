import functools as ft
import re
import math

class Node:
    def __init__(self, left_child = None, right_child = None):
        self.left = left_child
        self.right = right_child
    def __str__(self):
        return to_tower(self)
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.left == other.left and self.right == other.right


# ******************************
# *                            *
# *  tree -> string functions  *
# *                            *
# ******************************

# Params:
#   - node - a Node object
# Returns:
#   - the bracket representation of node (string)
#     e.g. (((1)(3))(4))
def to_bracket(node):
    return ('(' + ((to_bracket(node.left) if isinstance(node.left, Node) else '(' + str(node.left) + ')') if node.left is not None else '') +
                 ((to_bracket(node.right) if isinstance(node.right, Node) else '(' + str(node.right) + ')') if node.right is not None else '') + ')')

# recurse on given node
def _rec(func, node):
    if isinstance(node, Node):
        return func(node)
    elif isinstance(node, int) or isinstance(node, float):
        return str(node) if node >= 0 else '(' + str(node) + ')'
    return str(node)

# Params:
#   - node - a Node object
# Returns:
#   - the 'power tower' representation of node (string)
#     e.g. (1^3)^4
def to_tower(node):
    leftgood = (node.left is not None)
    rightgood = (node.right is not None)
    s = ''
    if leftgood:
        if rightgood and isinstance(node.left, Node):
            s += '(' + to_tower(node.left) + ')'
        else:
            s += _rec(to_tower, node.left)
    if rightgood:
        if leftgood:
            s += '^'
        # could add parens here to be completely unambiguous, but
        # by convention we can omit them: a^b^c = a^(b^c)
        s += _rec(to_tower, node.right)
    return s

# Params:
#   - node - a Node object
# Returns:
#   - the 'power tower' representation of node, but in LaTeX input form (string)
#     e.g. \left(1^{3}\right)^{4}
def to_LaTeX(node):
    leftgood = (node.left is not None)
    s = ''
    if leftgood:
        s += ( '\\left(' + to_LaTeX(node.left) + '\\right)' if isinstance(node.left, Node) else str(node.left) )
    if node.right is not None:
        if leftgood:
            s += '^{'
            s += _rec(to_LaTeX, node.right)
            s += '}'
        else:
            s += _rec(to_LaTeX, node.right)
    return s


# ******************************
# *                            *
# *  display tree (as a graph) *
# *                            *
# ******************************

# n spaces
def _nblanks(n):
    return ft.reduce((lambda x,y: x+y), [' ' for i in range(n)], '')

# Pads the string to have width=len2 and height=height
# Params:
#   - str1 - the string to pad
#   - len1 - length of str1
#   - len2 - the length to pad to
#   - side_to_pad - whether this is a left child ('L')
def _pad_sqare(str1, len1, len2, height, side_to_pad):
    str1 = re.split('\n',str1)
    for i in range(len(str1)):
        just_left = ( math.floor((len2-len1)/2) if side_to_pad == 'L' else math.ceil((len2-len1)/2) )
        str1[i] = str1[i].rjust(just_left+len1, ' ').ljust(len2, ' ')
    for i in range(height):
        try:
            temp = str1[i]
        except Exception as e:
            str1.append(_nblanks(len2))
    return str1

# Params:
#   - node - a Node object (or a leaf (string, int, float))
# Returns:
#   - an ascii image of the tree, e.g.
#             /\
#            /  \
#           /    \
#          /\     8
#         2  4                        (string)
# builds from leaves up, merging rectangles
def to_tree(node):
    if node is None:
        return None
    if not isinstance(node, Node):
        s = str(node)
        return (' ' + s + ' \n' + _nblanks(len(s)+2))
    ls = to_tree(node.left)
    rs = to_tree(node.right)
    if ls is None:
        if rs is None:
            return '/\\\n  '
        else:
            ls = re.sub(r'.', ' ', rs)
    else:
        if rs is None:
            rs = re.sub(r'.', ' ', ls)
    # pad the smaller one
    right_len = rs.index('\n')
    left_len = ls.index('\n')
    rs_split = rs.split('\n')
    ls_split = ls.split('\n')
    right_height = len(rs_split)
    left_height = len(ls_split)
    max_len = -2
    if left_len < right_len:
        ls = _pad_sqare(ls, left_len, right_len, right_height, 'L')
        rs = rs_split
        max_len = right_len
    elif left_len > right_len:
        ls = ls_split
        rs = _pad_sqare(rs, right_len, left_len, left_height, 'R')
        max_len = left_len
    else:
        ls = ls_split
        rs = rs_split
        max_len = right_len
    new_square = ['\n' + ls[i] + rs[i] for i in range(len(ls))]
    # make the branches
    left_branch = [('/'+_nblanks(i)).rjust(max_len, ' ') for i in range(math.floor(max_len/2))]
    right_branch = list(map(lambda x: re.sub('/', '\\\\', x[::-1]), left_branch))
    branches = [('\n' if i>0 else '') + left_branch[i] + right_branch[i] for i in range(len(left_branch))]
    branches.extend(new_square)
    branches = ft.reduce(lambda x,y: x+y, branches)
    return branches


# ******************************
# *                            *
# *  string -> tree functions  *
# *                            *
# ******************************

# Helper function for parse_ functions, tries to turn a string into an int or float
# Params:
#   - s - a string
# Returns:
#  - if s is tostring of an int, the int; else if of a flot, the float; else s.
def _parse_leaf(s):
    try:
        if '.' in s:
            s = float(s)
        else:
            s = int(s)
    except Exception as e: pass
    return s

# Params:
#   - s - a string of the power tower in bracket representation
#     e.g. (((1)(3))(4))
# Returns:
#   - the binary tree represented by s
#     e.g. Node(Node(1, 3), 4)
def parse_bracket(s):
    # can assume s has one of the forms:
    # (x) or ((x)(y)) or x
    le = len(s)
    if s[0] != '(' or s[le-1] != ')': return _parse_leaf(s)
    s = s[1:le-1]
    args = []
    parenLvl = start = 0
    for i in range(0, le-2):
        c = s[i]
        parenLvl += (1 if c == '(' else -1 if c == ')' else 0)
        if parenLvl == 0 and (c == ')' or i == le-3):
            args.append(s[start:i+1])
            start = i+1
        else: assert parenLvl >= 0 # imbalanced parentheses
    if len(args) == 1:
        s = s.replace('(','').replace(')','')
        return _parse_leaf(s)
    assert len(args) == 2 # only put 2 things in a pair of parentheses
    return Node(parse_bracket(args[0]), parse_bracket(args[1]))

# Params:
#   - s - a string of the power tower in bracket representation
#     e.g. (1^3)^4
# Returns:
#   - the binary tree represented by s
#     e.g. Node(Node(1, 3), 4)
def parse_tower(s):
    # can assume s has one of the forms:
    # x^y or (x^y) or (x) or x
    if '^' not in s:
        return _parse_leaf(s.replace('(', '').replace(')', ''))
    le = len(s)
    base = ''
    parenLvl = i = 0
    while True:
        c = s[i]
        parenLvl += (1 if c == '(' else -1 if c == ')' else 0)
        if parenLvl == 0 and (c == '^' or i == le-1):
            base = s[0:i+1]
            s = s[i+1:] # s is now the exponent
            if base[len(base)-1] == '^': base = base[0:len(base)-1]
            if s != '' and s[0] == '^':
                s = s[1:]
            break
        else: assert parenLvl >= 0 # imbalanced parentheses
        i += 1
    if s == '':
        return parse_tower(base[1:le-1])
    return Node(parse_tower(base), parse_tower(s))

# Params:
#   - s - a string of the power tower in LaTeX representation
#     e.g. \left(1^{3}\right)^{4}
# Returns:
#   - the binary tree represented by s
#     e.g. Node(Node(1, 3), 4)
def parse_LaTeX(s):
    return parse_tower(s.replace('\\left(', '(').replace('\\right)', ')').replace('{', '(').replace('}', ')'))


# testing 123
def _assertEq(a, b):
    if not a == b:
        print(str(a)+" =/= "+str(b))
def _test():
    trees = [
        Node(3.1, Node(4.1, Node(5.9, 2.6))),
        Node(2, Node(Node(3,5), Node(Node(Node('w','x'), 'y'), 'z'))),
        Node(1, Node(2, Node('a', Node('b', 'c')))),
        Node(Node(Node(Node(3, Node(1, 4)), Node(1, 5)), 9), Node(Node(2, 6), 5))
    ]
    # (bracket, tower, LaTeX)
    strings = [
        (
            '((3.1)((4.1)((5.9)(2.6))))',
            '3.1^4.1^5.9^2.6',
            '3.1^{4.1^{5.9^{2.6}}}'
        ),
        (
            '((2)(((3)(5))((((w)(x))(y))(z))))',
            '2^(3^5)^((w^x)^y)^z',
            '2^{\\left(3^{5}\\right)^{\\left(\\left(w^{x}\\right)^{y}\\right)^{z}}}'
        ),
        (
            '((1)((2)((a)((b)(c)))))',
            '1^2^a^b^c',
            '1^{2^{a^{b^{c}}}}'
        ),
        (
            '(((((3)((1)(4)))((1)(5)))(9))(((2)(6))(5)))',
            '(((3^1^4)^1^5)^9)^(2^6)^5',
            '\\left(\\left(\\left(3^{1^{4}}\\right)^{1^{5}}\\right)^{9}\\right)^{\\left(2^{6}\\right)^{5}}'
        )
    ]
    str_funcs = [to_bracket, to_tower, to_LaTeX]
    parse_funcs = [parse_bracket, parse_tower, parse_LaTeX]

    for i in range(0, len(trees)):
        tre = trees[i]
        tup = strings[i]
        # to_ functions
        for j in range(0, len(str_funcs)):
            _assertEq(str_funcs[j](tre), tup[j])
        # parse_ functions
        for j in range(0, len(parse_funcs)):
            _assertEq(parse_funcs[j](tup[j]), tre)
        #
    for j in range(0, len(str_funcs)):
        for k in range(0, len(parse_funcs)):
            _assertEq(str_funcs[j](parse_funcs[k](tup[k])), tup[j])

_test()
