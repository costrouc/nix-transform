import urllib.request
import zipfile
import time
import statistics

import pytest
from sly.lex import LexError

from nixfmt import NixLexer



@pytest.mark.parametrize('repo_url', [
    'https://github.com/NixOS/nixpkgs/archive/master.zip'
])
def test_benchmark_lexer(tmp_path, repo_url):


    zip_filename = tmp_path / 'temp.zip'
    with urllib.request.urlopen(repo_url) as response:
        with open(zip_filename, 'wb') as f:
            f.write(response.read())

    with zipfile.ZipFile(zip_filename) as f_zip:
        filenames = [_ for _ in f_zip.namelist() if _.endswith('.nix')]
        print(len(filenames), 'files to lex')

        successful = 0
        timings = []
        long_parse_times = []
        for i, filename in enumerate(filenames):
            with f_zip.open(filename) as f:
                contents = f.read().decode('utf8')
                lexer = NixLexer()
            try:
                start_time = time.time()
                tokens = tuple(lexer.tokenize(contents))
                successful += 1
            except Exception as e:
                print(f'({i}) {filename}')
                raise e
            finally:
                total = time.time() - start_time
                timings.append(total)
                if total > 0.2:
                    long_parse_times.append((filename, total))

    print(f'[{successful}/{len(filenames)}] succesfully lexed')
    print(f' total: {sum(timings)} [s]')
    print(f'   min: {min(timings)} [s]')
    print(f'   max: {max(timings)} [s]')
    print(f'  mean: {statistics.mean(timings)} [s]')
    print(f'median: {statistics.median(timings)} [s]')

    print('\nfiles with long parse times:')
    for filename, total in long_parse_times:
        print(f'{filename}: {total} [s]')
