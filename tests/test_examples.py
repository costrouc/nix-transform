import pytest

@pytest.mark.parametrize('filename', [
    'examples/nixpkgs-default.nix',
])
def test_lexer_files(lexer_tokens, filename):
    with open(filename) as f:
        lexer_tokens(f.read())
