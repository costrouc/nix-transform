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
])
def test_parser(parse, text, tree):
    print(text)
    print(tree)
    expected_tree = parse(text)
    print(expected_tree)
    assert expected_tree == tree
