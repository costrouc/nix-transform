from nixfmt import NixLexer
from nixfmt import NixParser

import pytest


@pytest.fixture
def lex():
    def _lex(text):
        lexer = NixLexer()
        return lexer.tokenize(text)
    return _lex


@pytest.fixture
def parse():
    def _parse(text):
        parser = NixParser()
        return parser.parse(text)
    return _parse
