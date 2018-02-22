"""
Computes ngram diversity.
"""

import code

# builtins
from typing import List, Set

# local
from common import Candidates, NgramResults


def run_ngram(txt: str, n: int) -> int:
    grams: Set[str] = set()
    for line in txt.splitlines():
        tkns = line.strip().split(' ')
        for start in range(len(tkns) - n + 1):
            grams.add(' '.join(tkns[start:start+n]))
    return len(grams)


def run_ngrams(txt: str, ns: List[int]) -> NgramResults:
    return {
        "gram": {n: run_ngram(txt, n) for n in ns}
    }

def ngrams(candidates: Candidates, ns: List[int] = [1,2,3,4]) -> None:
    for corpus in candidates['corpora'].values():
        corpus['ngrams'] = run_ngrams(corpus['contents'], ns)
