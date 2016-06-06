# -*- coding: utf-8 -*-

GRAMMAR_RELPATH0 = "data/mini-grammar-nonterminal-to-nonterminal"
GRAMMAR_RELPATH1 = "data/mini-grammar-nonterminal-to-terminal"

from waffle.math.combinations import generate_comb
import pandas as pd
import logging
import copy


def get_tables(path0, path1):
    grammar = pd.read_csv(path0)

    internal_table = {}
    for index, row in grammar.iterrows():
        if row["left"] not in internal_table:
            internal_table[row["left"]] = [row["right"]]
        else:
            internal_table[row["left"]].append(row["right"])

    grammar = pd.read_csv(path1)

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


# TODO: Should be renamed as SymbolNode (Parent Class: Node)
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

    # TODO: Should be moved into tree class
    def find_leaf_not_terminal(self, node):
        if node.is_leaf():
            return node.is_leaf_not_terminal()
        else:
            flag = False
            for n in node.get_children():
                flag = flag or self.find_leaf_not_terminal(n)
            return flag

    # TODO: Should be moved into tree class
    def has_leaf_not_terminal(self):
        return self.find_leaf_not_terminal(self)

    # TODO: Should be moved into tree class
    def is_parse_tree(self):
        return self.is_start() is True and self.has_leaf_not_terminal() is False

    def get_children(self):
        return self.children


# TODO: Should be renamed ParseTree (Parent Class: Tree)
class Tree(object):
    """
    Representation for a multi-tree
    """
    def __init__(self, root: Node, children=None):
        self.root = root
        self.children = children if children is not None else list()

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def add(self, *trees):
        self.children.extend(trees)

    @staticmethod
    def get_expections(node):
        expections = []
        if node.symbol in terminals:
            return expections
        if node.symbol in internal_table.keys():
            expections += internal_table[node.symbol]
        if node.symbol in terminal_table.keys():
            expections += terminal_table[node.symbol]
        return expections

    def get_expections_of_leaves(self):
        return [self.get_expections(x) for x in self.get_leaves()]

    @staticmethod
    def get_expection_comb(expections_ax):
        """
        expections_ax = [['that', 'this', 'a'], ['book', 'flight', 'meal', 'money']]
        """
        return generate_comb(expections_ax)

    def get_new_leaf_sets(self):
        expections_ax = self.get_expections_of_leaves()
        return Tree.get_expection_comb(expections_ax)

    def get_leaves(self)->Node:
        leaves = []

        def get_leaves_rec(node):
            if node.is_leaf():
                leaves.append(node)
            else:
                for n in node.get_children():
                    get_leaves_rec(n)

        get_leaves_rec(self.root)
        return leaves

    def is_parse_tree(self):
        return self.root.is_parse_tree()

    def get_children(self):
        return self.children


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


# TODO: Should be renamed into ParseTreeForest (Parent Class: Forest)
class Forest(object):
    def __init__(self, root: Tree):
        self.root = root

    def get_leaves(self)->Tree:
        leaves = []

        def get_leaves_rec(tree):
            if tree.is_leaf():
                leaves.append(tree)
            else:
                for n in tree.get_children():
                    get_leaves_rec(n)

        get_leaves_rec(self.root)
        return leaves

    def grow(self, tree: Tree):
        old_tree = copy.deepcopy(tree)
        new_leaf_sets = old_tree.get_new_leaf_sets()
        for leaves in new_leaf_sets:
            new_tree = Forest.generate_new_tree(old_tree, leaves)
            tree.add(new_tree)

    def grow_one_layer(self):
        leaves = self.get_leaves()
        for leaf in leaves:
            self.grow(leaf)

    def grow_complete_forest(self):
        while not self.is_complete_forest():
            self.grow_one_layer()

    def is_complete_forest(self):
        flag = True
        leaves = self.get_leaves()

        for leaf in leaves:
            f = leaf.is_parse_tree()
            if not leaf.is_parse_tree():
                flag = False
                return flag
        return flag

    @staticmethod
    def generate_new_tree(old_tree, leaves):
        tree = copy.deepcopy(old_tree)
        old_leaves = tree.get_leaves()
        if len(old_leaves) != len(leaves):
            print("Error, new leaves set length does not match length of old_leaves")
            raise Exception

        for i in range(len(old_leaves)):
            old_leaf = old_leaves[i]
            leaf_symbol = leaves[i]

            # skip terminals (leaf==None)
            if not leaf_symbol:
                continue
            if " " not in leaf_symbol:
                leaf = Node(leaf_symbol)
                old_leaf.add(leaf)
            else:
                tmps = leaf_symbol.split(" ")
                for tmp in tmps:
                    leaf = Node(tmp)
                    old_leaf.add(leaf)
        return tree


S = Node("S")
NP = Node("NP")
Det = Node("Det")
Nom = Node("Nom")
Noun = Node("Noun")
T1 = Node("a")
T2 = Node("flight")

#NP.add(Det, Noun)
S.add(NP)

print(S.is_parse_tree())

my_tree = Tree(S)
forest = Forest(my_tree)
#forest.grow_one_layer()
forest.grow_complete_forest()

axxfef = 1


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