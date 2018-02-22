# text-metrics
Automatic text metrics

## Usage

```bash
# Compares each candidate (c) separately against all references (r).
python textmetrics/main.py c1.txt c2.txt --references r1.txt r2.txt r3.txt
```

## Installation

Requires:
- Perl
- Python 3.6+

After cloning the repo, run:

```bash
pip install requirements.txt
```

## Features

- [x] BLEU
