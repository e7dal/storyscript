# -*- coding: utf-8 -*-
from lark import Lark
from lark.common import UnexpectedToken

from .grammar import Grammar
from .indenter import CustomIndenter
from .transformer import Transformer


class Parser:

    def __init__(self, algo='lalr'):
        self.algo = algo
        self.grammar = Grammar()

    def indenter(self):
        return CustomIndenter()

    def transformer(self):
        return Transformer()

    def lark(self):
        grammar = self.grammar.build()
        return Lark(grammar, parser=self.algo, postlex=self.indenter())

    def parse(self, source, json=False):
        lark = self.lark()
        try:
            tree = lark.parse(source)
        except UnexpectedToken:
            return None
        transformed_tree = self.transformer().transform(tree)
        if json:
            return transformed_tree.json()
        return transformed_tree

    def lex(self, source):
        return self.lark().lex(source)
