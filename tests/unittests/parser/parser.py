# -*- coding: utf-8 -*-
from lark import Lark
from lark.common import UnexpectedToken

from pytest import fixture, raises

from storyscript.parser import CustomIndenter, Grammar, Parser, Transformer


@fixture
def parser(magic):
    parser = Parser()
    parser.grammar = magic()
    return parser


def test_parser_init(patch):
    patch.init(Grammar)
    parser = Parser()
    assert isinstance(parser.grammar, Grammar)
    assert parser.algo == 'lalr'


def test_parser_init_algo(patch):
    patch.init(Grammar)
    parser = Parser(algo='algo')
    assert parser.algo == 'algo'


def test_parser_indenter(patch, parser):
    patch.init(CustomIndenter)
    assert isinstance(parser.indenter(), CustomIndenter)


def test_parser_transfomer(patch, parser):
    patch.init(Transformer)
    assert isinstance(parser.transformer(), Transformer)


def test_parser_lark(patch, parser):
    patch.init(Lark)
    patch.object(Parser, 'indenter')
    result = parser.lark()
    Lark.__init__.assert_called_with(parser.grammar.build(),
                                     parser=parser.algo,
                                     postlex=Parser.indenter())
    assert isinstance(result, Lark)


def test_parser_parse(patch, parser):
    """
    Ensures the build method can build the grammar
    """
    patch.many(Parser, ['lark', 'transformer'])
    result = parser.parse('source')
    Parser.lark().parse.assert_called_with('source')
    Parser.transformer().transform.assert_called_with(Parser.lark().parse())
    assert result == Parser.transformer().transform()


def test_parser_parse_json(patch, parser):
    patch.many(Parser, ['lark', 'transformer'])
    result = parser.parse('source', json=True)
    assert result == Parser.transformer().transform().json()


def test_parser_parse_unexpected_token(patch, parser):
    patch.init(Lark)
    patch.object(Lark, 'parse', side_effect=UnexpectedToken('', '', '', ''))
    patch.many(Parser, ['indenter', 'transformer'])
    assert parser.parse('source') is None


def test_parser_lex(patch, parser):
    patch.many(Parser, ['lark', 'indenter'])
    result = parser.lex('source')
    Parser.lark().lex.assert_called_with('source')
    assert result == Parser.lark().lex()
