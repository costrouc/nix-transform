import zipfile
import urllib.request
import urllib.error
import tempfile
import socket
import os

from nixfmt import NixLexer

def find_https_urls(filename, contents):
    lexer = NixLexer()

    tokens = tuple(lexer.tokenize(contents))
    uris = [t.value for t in tokens if t.type == 'URI' and t.value.startswith('http://')]
    for uri in uris:
        https_uri = uri.replace('http://', 'https://')
        try:
            with urllib.request.urlopen(https_uri, timeout=1.0) as response:
                if response.getcode() == 200:
                    print(f'VALID   {https_uri}')
                else:
                    print(f'INVALID {https_uri}')
        except (urllib.error.URLError, socket.timeout):
            print(f'INVALID {https_uri}')


def main():
    repo_url = 'https://github.com/NixOS/nixpkgs/archive/master.zip'

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_filename = f'{tmpdir}/repo.zip'
        with urllib.request.urlopen(repo_url) as response:
            with open(zip_filename, 'wb') as f:
                f.write(response.read())

        with zipfile.ZipFile(zip_filename) as f_zip:
            filenames = [_ for _ in f_zip.namelist() if _.endswith('.nix')]
            for filename in filenames:
                with f_zip.open(filename) as f:
                    find_https_urls(filename, f.read().decode('utf8'))



if __name__ == '__main__':
    main()
