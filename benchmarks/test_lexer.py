import urllib.request
import zipfile
import time

import pytest

from nixfmt import NixLexer


@pytest.mark.parametrize('repo_url', [
    'https://github.com/NixOS/nixpkgs/archive/master.zip'
])
def test_benchmark_lexer(tmp_path, repo_url):
    lexer = NixLexer()

    zip_filename = tmp_path / 'temp.zip'
    with urllib.request.urlopen(repo_url) as response:
        with open(zip_filename, 'wb') as f:
            f.write(response.read())

    with zipfile.ZipFile(zip_filename) as f_zip:
        filenames = [_ for _ in f_zip.namelist() if _.endswith('.nix')]
        print(len(filenames), 'files to lex')
        start_time = time.time()
        for i, filename in enumerate(filenames):
            print(f'({i}): {filename}')
            with f_zip.open(filename) as f:
                contents = f.read().decode('utf8')
                # print(contents)
            tokens = tuple(lexer.tokenize(contents))
            # print([t for t in tokens if t.type == 'URI' and t.value.startswith('http://')])

        print(time.time() - start_time, 'seconds')
        assert False
