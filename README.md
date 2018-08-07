# textmetrics

Automatic text metrics---BLEU, ROUGE, and METEOR, plus extras like vocab and
ngrams.

## Usage

```bash
# Compares each candidate (c) separately against all references (r).
python textmetrics/main.py c1.txt c2.txt --references r1.txt r2.txt r3.txt
```

## Installation

Requires:
- Perl (for BLEU)
- Java 1.8 (for METEOR)
- Python 3.6+

After cloning the repo, run:

```bash
pip install requirements.txt
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
