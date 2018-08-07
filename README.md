# textmetrics

Automatic text metrics---BLEU, ROUGE, and METEOR, plus extras like vocab and
ngrams.

## Usage

```bash
# Compares each candidate (c) separately against all references (r).
python -m textmetrics.main c1.txt c2.txt --references r1.txt r2.txt r3.txt
```

## Installation

Requires:
- Perl (for BLEU)
- Java 1.8 (for METEOR)
- Python 3.6+

```bash
pip install textmetrics
```

## Features

- [x] BLEU
- [x] ROUGE
- [x] METEOR


## Notes

BLEU and METEOR use the refernce implementations (in Perl and Java,
respectively). We originally used the reference Perl implementation for ROUGE
as well, but it ran so slowly that we opted for a Python reimplementation
instead. (ROUGE's original Perl implementation is also more difficult to setup,
even with wrapper libraries.)

## Worklist

- [ ] pypi

- [ ] API support

- [ ] ROUGE crashes things if it decides there aren't sentences (e.g., run with
  README.md as input and reference)

- [ ] Add back in orig ROUGE for completeness (place behind switch)

- [ ] ngrams has divide by zero error. With two simple files (two lines each,
  same first line, differing second line) running with `2.txt --references
  1.txt 1.txt` triggered this divide by zero

- [ ] Demo for better README

- [ ] Tests

- [ ] Early check in each module for whether program runnable + nice error
  message (e.g., no java or bad version, no perl or bad version, etc.)


Note to self: I followed this guide for [packaging to
pypi](https://packaging.python.org/tutorials/packaging-projects/), and future
uploads will probably look like:

```bash
# (1) ensure tests pass

# (2) bump version in setup.py

# (3) commit + push to github

# (4) generate distribution
python setup.py sdist bdist_wheel

# (5) Upload
twine upload dist/*
```
