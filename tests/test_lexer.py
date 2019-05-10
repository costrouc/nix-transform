import pytest
import itertools

from nixfmt import NixLexer


@pytest.mark.parametrize('text,tokens', [
    # values
    ('null', ('NULL',)),
    ('true', ('TRUE',)),
    ('false', ('FALSE',)),
    ('asdf', ('ID',)),
    ('12345', ('INT',)),
    ('1123.123', ('FLOAT',)),
    (r'"\n"', ('STRING_QUOTE', 'STRING', 'STRING_QUOTE')),
    (r'"asdf$"', ('STRING_QUOTE', 'STRING', 'STRING', 'STRING_QUOTE')),
    ('"asdf"', ('STRING_QUOTE', 'STRING', 'STRING_QUOTE')),
    (r'"a\"sd\"f"', ('STRING_QUOTE', 'STRING', 'STRING_QUOTE')),
    ('''"multi
line
string
"''', ('STRING_QUOTE', 'STRING', 'STRING_QUOTE')),
    ('''\'\'multi
line
string
\'\'''', ('INDENTED_STRING_QUOTE', 'INDENTED_STRING', 'INDENTED_STRING_QUOTE')),
    ("''this'is'a'string''", ('INDENTED_STRING_QUOTE', 'INDENTED_STRING', 'INDENTED_STRING_QUOTE')),
    # paths
    ('./.', ('PATH',)), ('/home/user/.config/', ('PATH',)),
    ('~/scratch', ('HPATH',)), ('~/scratch/', ('HPATH',)),
    ('<nixpkgs>', ('SPATH',)),
    ('# ${true} this is a comment ####', ('COMMENT',)),
    ('''/* this
is if else
a comment
*/''', ('COMMENT',)),
    ('https://github.com/nixos/nixpkgs', ('URI',)),
    # keywords
    ('abort', ('ABORT',)),
    ('assert', ('ASSERT',)),
    ('import', ('IMPORT',)),
    ('inherit', ('INHERIT',)),
    ('with', ('WITH',)),
    ('let', ('LET',)),
    ('in', ('IN',)),
    ('if', ('IF',)),
    ('then', ('THEN',)),
    ('else', ('ELSE',)),
    ('rec', ('REC',)),
    ('or', ('OR_KW',)),
    # comparison
    ('==', ('EQ',)),
    ('=', ('ASSIGN',)),
    ('!=', ('NEQ',)),
    ('<=', ('LEQ',)),
    ('<', ('LESS',)),
    ('>=', ('GEQ',)),
    ('>', ('GREATER',)),
    ('&&', ('AND',)),
    ('||', ('OR',)),
    # operations
    ('->', ('IMPL',)),
    ('//', ('UPDATE',)),
    ('++', ('CONCAT',)),
    ('!', ('NOT',)),
    ('+', ('PLUS',)),
    ('-', ('MINUS',)),
    ('*', ('TIMES',)),
    ('/', ('DIVIDE',)),
    ('?', ('DEFAULT',)),
    (',', ('COMMA',)),
])
def test_lexer(lexer_tokens, text, tokens):
    print('text:', text)
    print('tokens:', tokens)
    expected_tokens = tuple(_.type for _ in lexer_tokens(text))
    print('expected:', expected_tokens)
    assert tokens == expected_tokens


@pytest.mark.parametrize('text,tokens', [
    ('asdf.qwer', ('ID', 'DOT', 'ID')),
    ('1 + 2', ('INT', 'WHITESPACE', 'PLUS', 'WHITESPACE', 'INT')),
    ('import ./nixpkgs', ('IMPORT', 'WHITESPACE', 'PATH')),
    ('{a =1; }', ('LBRACE', 'ID', 'WHITESPACE', 'ASSIGN', 'INT', 'SEMICOLON', 'WHITESPACE', 'RBRACE')),
    ('''
# this is a comment
{a=1;}/*
this
is a
comment
*/''', ('WHITESPACE', 'COMMENT', 'WHITESPACE',
      'LBRACE', 'ID', 'ASSIGN', 'INT', 'SEMICOLON', 'RBRACE',
      'COMMENT')),
    ('[1 2]', ('LBRACKET', 'INT', 'WHITESPACE', 'INT', 'RBRACKET')),
    ('if true then 1 else 2', ('IF', 'WHITESPACE', 'TRUE', 'WHITESPACE', 'THEN', 'WHITESPACE', 'INT', 'WHITESPACE', 'ELSE', 'WHITESPACE', 'INT')),
    ('''{ ... }:
rec {}''', ('LBRACE', 'WHITESPACE', 'ELLIPSIS', 'WHITESPACE', 'RBRACE', 'COLON', 'WHITESPACE',
            'REC', 'WHITESPACE', 'LBRACE', 'RBRACE')),
    # no dollar at end of string
    ('"asdf${0}"', ('STRING_QUOTE', 'STRING', 'DOLLAR_LBRACE', 'INT', 'RBRACE', 'STRING_QUOTE')),
    ("''asdf${0}''", ('INDENTED_STRING_QUOTE', 'INDENTED_STRING', 'DOLLAR_LBRACE', 'INT', 'RBRACE', 'INDENTED_STRING_QUOTE')),
    # dollar at end of string
    ('"asdf$${0}"', ('STRING_QUOTE', 'STRING', 'STRING', 'DOLLAR_LBRACE', 'INT', 'RBRACE', 'STRING_QUOTE')),
    ("''asdf$${0}''", ('INDENTED_STRING_QUOTE', 'INDENTED_STRING', 'INDENTED_STRING', 'DOLLAR_LBRACE', 'INT', 'RBRACE', 'INDENTED_STRING_QUOTE')),
    ('''''
      mkdir -p $out/bin
      install -D $src $out/libexec/php-cs-fixer/php-cs-fixer.phar
      makeWrapper ${php}/bin/php $out/bin/php-cs-fixer \
        --add-flags "$out/libexec/php-cs-fixer/php-cs-fixer.phar"
    '';''', ('INDENTED_STRING_QUOTE', 'INDENTED_STRING', 'DOLLAR_LBRACE', 'ID', 'RBRACE', 'INDENTED_STRING', 'INDENTED_STRING_QUOTE', 'SEMICOLON')),
])
def test_complex_tokens(lexer_tokens, text, tokens):
    print('text:', text)
    print('tokens:', tokens)
    expected_tokens = tuple(_.type for _ in lexer_tokens(text))
    print('expected:', expected_tokens)
    assert tokens == expected_tokens
