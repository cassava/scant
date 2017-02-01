scant
======

This is a small collection of scripts to streamline and simplify scanning
documents.

The scant scripts are distributed under the [MIT License](LICENSE).

### Installation

There is no installation necessary, just make sure you have
[Python 3](www.python.org) installed.
Currently the scripts make use of SANE and ImageMagick, so these are
also dependencies.

### Usage
The primary script for initiating scans is `scant.py`. It can be configured
with various settings. I suggest you modify the script so it speaks to your
scanner by default. Then, run the script and enter your filenames:

```
$ ./scant.py
scant usage: [option,...>]filename[.format]
> First file
> 150>Second file (150dpi)
> a5>A5 document
> a5,75>Don't need much here
> [Ctrl+D]
```

Enjoy!
