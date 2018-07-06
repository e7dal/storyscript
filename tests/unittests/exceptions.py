# -*- coding: utf-8 -*-
from pytest import fixture

from storyscript.exceptions import StoryError


@fixture
def error(magic):
    return StoryError(0, magic(spec=['line', 'column']))


def test_exceptions_storyerror_init():
    error = StoryError(0, 'item')
    assert error.error_type == 0
    assert error.item == 'item'
    assert issubclass(StoryError, SyntaxError)


def test_exceptions_storyerror_reason(error):
    assert error.reason() == 'unknown'


def test_exceptions_storyerror_token_message(error):
    expected = ('Failed reading story because of unexpected "value" at '
                'line 1, column 2')
    assert error.token_message('value', 1, 2) == expected


def test_exceptions_storyerror_tree_message(error):
    expected = ('Failed reading story because of unexpected "value" at '
                'line 1')
    assert error.tree_message('value', 1) == expected


def test_exceptions_storyerror_pretty_token(patch, error):
    patch.object(StoryError, 'token_message')
    error.error_type = 'unknown'
    result = error.pretty()
    args = (error.item, error.item.line, error.item.column)
    StoryError.token_message.assert_called_with(*args)
    assert result == StoryError.token_message()


def test_exceptions_storyerror_pretty_tree(patch, error):
    patch.object(StoryError, 'tree_message')
    error.item.data = 'data'
    error.error_type = 'unknown'
    result = error.pretty()
    args = (error.item, error.item.line())
    StoryError.tree_message.assert_called_with(*args)
    assert result == StoryError.tree_message()


def test_exceptions_storyerror_pretty_reason(patch, error):
    patch.many(StoryError, ['token_message', 'reason'])
    result = error.pretty()
    args = (error.item, error.item.line, error.item.column)
    StoryError.token_message.assert_called_with(*args)
    assert result == '{}. Reason: {}'.format(StoryError.token_message(),
                                             StoryError.reason())


def test_exceptions_storyerror_str_(patch, error):
    patch.object(StoryError, 'pretty', return_value='pretty')
    assert str(error) == StoryError.pretty()
