# -*- coding: utf-8 -*-

GRAMMAR_RELPATH0 = "data/mini-grammar-nonterminal-to-nonterminal"
GRAMMAR_RELPATH1 = "data/mini-grammar-nonterminal-to-terminal"

from waffle import system
import pandas as pd
import logging


def get_tables(path0, path1):
    grammar_file_pth = system.abs_path(path0)
    grammar = pd.read_csv(grammar_file_pth)

    internal_table = {}
    for index, row in grammar.iterrows():
        if row["left"] not in internal_table:
            internal_table[row["left"]] = [row["right"]]
        else:
            internal_table[row["left"]].append(row["right"])

    grammar_file_pth = system.abs_path(path1)
    grammar = pd.read_csv(grammar_file_pth)

    terminal_table = {}
    for index, row in grammar.iterrows():
        if row["left"] not in terminal_table:
            terminal_table[row["left"]] = [row["right"]]
        else:
            terminal_table[row["left"]].append(row["right"])
    return internal_table, terminal_table

internal_table, terminal_table = get_tables(GRAMMAR_RELPATH0, GRAMMAR_RELPATH1)

print(internal_table)
print(terminal_table)


def get_terminals(terminal_table):
    terminals = []
    for values in terminal_table.values():
        terminals.extend(values)
    terminals = set(terminals)
    return terminals

terminals = get_terminals(terminal_table)

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

    def is_parse_tree(self):
        return self.is_start() is True and self.has_leaf_not_terminal() is False

    def get_children(self):
        return self.children


class Tree(object):
    """
    Representation for a multi-tree
    """
    def __init__(self, root, children=None):
        self.root = root
        if children:
            self.children = children
        else:
            self.children = []

    def expand_self(self):
        """
        This method generates several expansions from a tree
        """
        node_list = []
        if self.is_leaf():
            print("Leaf node can not be expanded")
            raise Exception
        """
        for descendant in self.descendants:
            new_node =
        """

    def get_expections(self, node):
        expections = []
        if node.symbol in internal_table.keys():
            expections += internal_table[node.symbol]
        if node.symbol in terminal_table.keys():
            expections += terminal_table[node.symbol]
        return expections


    def get_leaves(self):
        leaves = []
        def get_leaves_rec(node):
            if node.is_leaf():
                leaves.append(node)
            else:
                for n in node.get_children():
                    get_leaves_rec(n)

        return get_leaves_rec(self.root)


class ParseTree(object):
    """
    A wrapper of the root node (which is the equivalent of a parse tree)
    """
    def __init__(self, root):
        if not hasattr(root, "is_parse_tree"):
            logging.error("Root given is not a valid node object")
            raise Exception
        if root.is_parse_tree():
            self.root = root
        else:
            logging.error("Root given is not a parse tree equivalent node")
            raise Exception


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

print(S.is_parse_tree())


def build_all_parse_trees(internal_table, terminal_table):
    """ Build All possible parse trees from grammars """
    parse_tree_tmps = []

    parse_tree_tmp = []
    if 'S' not in internal_table.keys():
        logging.error("No root node 'S' in grammar")
        raise Exception
    else:
        parse_tree_tmp.append(Node("S"))
    parse_tree_tmps.append(parse_tree_tmp)

    parse_tree_tmp = []
    for inte in internal_table["S"]:
        children = []
        symbols = inte.split(" ")
        for symbol in symbols:
            children.append(Node(symbol))
        parse_tree_tmp.append(Node("S", children=children))