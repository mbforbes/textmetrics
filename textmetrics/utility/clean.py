"""
Removes special tokens. Assumes tokenized text.
"""

import io
from typing import Set

DEFAULT_FILE = 'textmetrics/utility/clean_tokens.txt'

def load(f: io.TextIOWrapper) -> Set[str]:
    """Reads `fn` and returns a set of its lines."""
    return {line.strip() for line in f.readlines()}


def clean(body: str, removal: Set[str]) -> str:
    """Removes all tokens in `removal` from `body`.

    Assumes `body` is already tokenized."""
    lines = []
    for line in body.split('\n'):
        lines.append(' '.join([tkn for tkn in line.split(' ') if tkn not in removal]))
    return '\n'.join(lines)
