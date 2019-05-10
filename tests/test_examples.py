import pytest

from nixfmt import NixLexer


@pytest.mark.parametrize('filename', [
    'examples/nix/default.nix',
    'examples/nix/simple.nix',
    'examples/nix/zram.nix',
    'examples/nix/zfs.nix'
])
def test_examples(lexer_tokens, filename):
    with open(filename) as f:
        contents = f.read()

    print(f'\nBEGIN {filename}')
    for token in lexer_tokens(contents):
        if token.type in {'WHITESPACE', 'STRING', 'INDENTED_STRING'}:
            print(f'token ({token.type}): {repr(token.value)}')
        else:
            print(f'token ({token.type}): {repr(token.value)[1:-1]}')
