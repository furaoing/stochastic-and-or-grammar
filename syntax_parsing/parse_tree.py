# -*- coding: utf-8 -*-

GRAMMAR_RELPATH0 = "data/mini-grammar-nonterminal-to-nonterminal"
GRAMMAR_RELPATH1 = "data/mini-grammar-nonterminal-to-terminal"

from waffle import system
import pandas as pd

test_str = "Book that flight"

grammar_file_pth = system.abs_path(GRAMMAR_RELPATH0)
grammar = pd.read_csv(grammar_file_pth)

internal_table = {}
for index, row in grammar.iterrows():
    if row["left"] not in internal_table:
        internal_table[row["left"]] = [row["right"]]
    else:
        internal_table[row["left"]].append(row["right"])

grammar_file_pth = system.abs_path(GRAMMAR_RELPATH1)
grammar = pd.read_csv(grammar_file_pth)

terminal_table = {}
for index, row in grammar.iterrows():
    if row["left"] not in terminal_table:
        terminal_table[row["left"]] = [row["right"]]
    else:
        terminal_table[row["left"]].append(row["right"])

print(internal_table)
print(terminal_table)

terminals = []
for values in terminal_table.values():
    terminals.extend(values)
terminals = set(terminals)

"""
class Production(object):
    def __init__(self, *terms):
        self.terms = terms

    def __len__(self):
        return len(self.terms)

    def __getitem__(self, index):
        return self.terms[index]

    def __iter__(self):
        return iter(self.terms)

    def __repr__(self):
        return " ".join(str(t) for t in self.terms)

    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.terms)


class Rule(object):
    def __init__(self, name, *productions):
        self.name = name
        self.productions = list(productions)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))

    def add(self, *productions):
        self.productions.extend(productions)
"""


class Node(object):
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        # Equivalent of value of each node in b-tree
        self.name = self.symbol
        if children:
            self.children = children
        else:
            self.children = []

    def add(self, *nodes):
        self.children.extend(nodes)

    def is_terminal(self):
        if self.symbol in terminals:
            return True
        else:
            return False

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def is_start(self):
        return self.symbol == "S"

    def is_leaf_terminal(self):
        return self.is_leaf() and self.is_terminal()

    def is_leaf_not_terminal(self):
        return self.is_leaf() is True and self.is_terminal() is False

    def find_leaf_not_terminal(self, node):
        if node.is_leaf():
            return node.is_leaf_not_terminal()
        else:
            flag = False
            for n in node.get_children():
                flag = flag or self.find_leaf_not_terminal(n)
            return flag

    def has_leaf_not_terminal(self):
        return self.find_leaf_not_terminal(self)

    def is_tree(self):
        return self.is_start() is True and self.has_leaf_not_terminal() is False

    def get_children(self):
        return self.children


S = Node("S")
NP = Node("NP")
Det = Node("Det")
Nom = Node("Nom")
Noun = Node("Noun")
T1 = Node("a")
T2 = Node("flight")

Noun.add(T2)
Nom.add(Noun)
Det.add(T1)
NP.add(Det, Noun)
S.add(NP)

print(S.has_leaf_not_terminal())
print(S.is_tree())
"""
    def expand(self):
        node_list = []
        if self.is_leaf():
            print("Leaf node can not be expanded")
            raise Exception
        for descendant in self.descendants:
            new_node =
"""

"""
def parse(internals_table, leaves_table, text=None):
    parse_trees = []
    parse_trees1 = []

    if 'S' not in internals_table.keys():
        logging.error("No root node 'S' in grammar")
        raise Exception
    else:
        parse_trees.append(Node("S"))

    for inte in internal_table["S"]:
        descendants = []
        symbols = inte.split(" ")
        for symbol in symbols:
            descendants.append(Node(symbol))
        parse_trees1.append(Node("S", descendants=descendants))
    print(parse_trees1)


parse(internal_table, terminal_table)
"""