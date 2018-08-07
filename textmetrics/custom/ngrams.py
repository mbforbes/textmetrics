"""
Computes ngram diversity.
"""

# builtins
from collections import Counter
import typing
from typing import List, Set, Tuple

# local
from textmetrics.common import Candidates, NgramResults


def line_ngrams(line: str, n: int) -> typing.Counter[str]:
    """Returns Counter of `n`-grams in `line`."""
    grams: typing.Counter[str] = Counter()
    tkns = line.strip().split(' ')
    for start in range(len(tkns) - n + 1):
        grams[' '.join(tkns[start:start+n])] += 1
    return grams


def get_ngram_stats(txt: str, n: int) -> Tuple[float, float, float, int, int, float]:
    """Returns: (
        per-line average unique `n`-grams,
        per-line average total `n`-grams,
        per-line average ratio unique / total `n`-grams,
        overall number unique `n`-grams,
        overall number total `n`-grams,
        overall average unique / total `n`-grams,
    """
    # track overall
    overall: typing.Counter[str] = Counter()

    # also track per-line
    perline_unique, perline_total, n_lines = 0, 0, 0

    # run over text
    for line in txt.splitlines():
        # get ngrams for line
        line_grams = line_ngrams(line, n)

        # bookkeep overall
        overall += line_grams

        # bookkeep per-line
        perline_unique += len(line_grams)
        perline_total += sum(line_grams.values())
        n_lines += 1

    # compute and return
    overall_unique = len(overall)
    overall_total = sum(overall.values())
    return (
        perline_unique / n_lines,
        perline_total / n_lines,
        perline_unique / perline_total,
        overall_unique,
        overall_total,
        overall_unique / overall_total,
    )


def run_ngrams(txt: str, ns: List[int]) -> NgramResults:
    res: NgramResults = {
        'perline_avg_unique': {},
        'perline_avg_total': {},
        'perline_avg_ratio': {},
        'overall_unique': {},
        'overall_total': {},
        'overall_ratio': {},
    }
    for n in ns:
        stats = get_ngram_stats(txt, n)
        res['perline_avg_unique'][n] = stats[0]
        res['perline_avg_total'][n] = stats[1]
        res['perline_avg_ratio'][n] = stats[2]
        res['overall_unique'][n] = stats[3]
        res['overall_total'][n] = stats[4]
        res['overall_ratio'][n] = stats[5]
    return res


def ngrams(candidates: Candidates, ns: List[int] = [1,2,3,4]) -> None:
    for corpus in candidates['corpora'].values():
        corpus['ngrams'] = run_ngrams(corpus['contents'], ns)
