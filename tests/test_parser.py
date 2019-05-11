import pytest


@pytest.mark.parametrize('text,tree', [
    # simple math
    ('1+2', ('PLUS', ('INT', '1'), ('INT', '2'))),
    ('1.0-2.11', ('SUBTRACT', ('FLOAT', '1.0'), ('FLOAT', '2.11'))),
    ('1.0*2.11', ('TIMES', ('FLOAT', '1.0'), ('FLOAT', '2.11'))),
    ('1.0/ 2.11', ('DIVIDE', ('FLOAT', '1.0'), ('FLOAT', ('WHITESPACE', ' '), '2.11'))),
    ('1.0  / 2.11', ('DIVIDE', ('FLOAT', '1.0', ('WHITESPACE', '  ')), ('FLOAT', ('WHITESPACE', ' '), '2.11'))),
    ('a.b.c', ('ATTRIBUTE', 'a', 'b', 'c')),
    ('a.b.${foo}', ('ATTRIBUTE', 'a', 'b', ('EXPRESSION', ('ATTRIBUTE', 'foo')))),
    ('a + b # asdf', ('PLUS', ('ATTRIBUTE', 'a', ('WHITESPACE', ' ')), ('ATTRIBUTE', ('WHITESPACE', ' '), 'b', ('WHITESPACE', ' '), ('COMMENT', '# asdf')))),
    ('a /* qwer */+ b # asdf', ('PLUS', ('ATTRIBUTE', 'a', ('WHITESPACE', ' '), ('COMMENT', '/* qwer */')), ('ATTRIBUTE', ('WHITESPACE', ' '), 'b', ('WHITESPACE', ' '), ('COMMENT', '# asdf')))),
    ('a = 1', ('ASSIGN', ('ATTRIBUTE', 'a', ('WHITESPACE', ' ')), ('INT', ('WHITESPACE', ' '), '1'))),
    ('if a then b else c', ('IF',
                            ('ATTRIBUTE', ('WHITESPACE', ' '), 'a', ('WHITESPACE', ' ')),
                            ('ATTRIBUTE', ('WHITESPACE', ' '), 'b', ('WHITESPACE', ' ')),
                            ('ATTRIBUTE', ('WHITESPACE', ' '), 'c'))),
    ('import ./.', ('IMPORT', ('PATH', ('WHITESPACE', ' '), './.'))),
    ('import ~/scratch', ('IMPORT', ('HPATH', ('WHITESPACE', ' '), '~/scratch'))),
    ('import <nixpkgs>', ('IMPORT', ('SPATH', ('WHITESPACE', ' '), '<nixpkgs>'))),
    ('import https://github.com/nixos/nixpkgs', ('IMPORT', ('URI', ('WHITESPACE', ' '), 'https://github.com/nixos/nixpkgs'))),
])
def test_parser(parse, text, tree):
    print(text)
    print(tree)
    expected_tree = parse(text)
    print(expected_tree)
    assert expected_tree == tree
