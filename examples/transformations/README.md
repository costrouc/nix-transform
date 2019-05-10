# Example Transformations

# http to https

This is a quick script that downloads the current nixpkgs repository
and checks every nix file for a uri that is `http://` and checks if
the secure url `https://` works. For sanity a 1 second timeout is used
on all url calls.

```
python examples/transformations/http_to_https.py
```

Just a snippet of the result

```
...
VALID   https://www.aeon.cash/
VALID   https://www.bitcoin.org/
INVALID https://www.dogecoin.com/
INVALID https://freicoi.in/
VALID   https://www.bitcoin.org/
INVALID https://parity.io
INVALID https://parity.io
INVALID https://wownero.org/
VALID   https://kokkinizita.linuxaudio.org/linuxaudio/ladspa/index.html
VALID   https://kokkinizita.linuxaudio.org/linuxaudio/ladspa/index.html
VALID   https://www.mellowood.ca/mma/index.html
VALID   https://abcde.einval.com/wiki/
VALID   https://kokkinizita.linuxaudio.org/linuxaudio/aeolus/index.html
INVALID https://aj-snapshot.sourceforge.net/
VALID   https://objectivewave.wordpress.com/ams-lv2
VALID   https://ardour.org/
INVALID https://ario-player.sourceforge.net/
...
```
