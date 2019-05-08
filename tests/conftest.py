from nixfmt import NixLexer

import pytest


@pytest.fixture
def lexer():
    lexer = NixLexer()
    return lexer


@pytest.fixture
def lexer_tokens(lexer):
    def _lexer_tokens(text):
        return lexer.tokenize(text)
    return _lexer_tokens
