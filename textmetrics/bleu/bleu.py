"""
Simply wraps the BLEU perl script (multi-bleu.perl).
"""

# builtins
import code
import os
import subprocess
from typing import List

# local
from textmetrics.common import References, Candidates, BLEUResults


def extract_res(raw_output: bytes) -> BLEUResults:
    """Turns raw output from multi-bleu.perl script into BLEUResults format."""
    output = str(raw_output)

    #
    # example:
    #
    # "b'BLEU = 100.00, 100.0/100.0/100.0/100.0 (BP=1.000, ratio=1.000, hyp_len=11, ref_len=11)\\n'"
    #

    s1, s2 = output.split('(')

    # handle s1: overall and bleu-1..4 scores
    overall_section, ngram_section = s1.split(',')
    overall = float(overall_section.split('=')[1].strip())
    subscores = [float(s) for s in ngram_section.strip().split('/')]

    # handle s2: the sore breakdown in parentheses
    s2_contents, _ = s2.split(')')
    s2_pieces = [piece.strip() for piece in s2_contents.split(',')]
    bp = float(s2_pieces[0].split('=')[1])
    len_ratio = float(s2_pieces[1].split('=')[1])
    can_len = int(s2_pieces[2].split('=')[1])
    ref_len = int(s2_pieces[3].split('=')[1])

    return {
        'overall': overall,
        'bleu1': subscores[0],
        'bleu2': subscores[1],
        'bleu3': subscores[2],
        'bleu4': subscores[3],
        'brevity_penalty': bp,
        'length_ratio': len_ratio,
        'candidate_length': can_len,
        'reference_length': ref_len,
    }


def run_bleu(reference_fns: List[str], candidate_fn: str,
             script: str = 'textmetrics/bleu/multi-bleu.perl') -> BLEUResults:
    """Runs `script` to compute BLEU scores for the file name candidate_fn
    given reference filenames `reference_fns`."""
    with open(candidate_fn, 'r') as in_f:
        res = subprocess.run(
            ['perl', script] + reference_fns,
            stdin=in_f,
            stdout=subprocess.PIPE,
        )
    return extract_res(res.stdout)


def bleu(references: References, candidates: Candidates) -> None:
    """Runs each of `candidates` against all `references` separately.

    Writes results into candidates['bleu'].
    """
    # Compute bleu for each candidate separately against all references
    ref_fns = [ref['tmpfile'] for ref in references['corpora'].values()]
    for corpus in candidates['corpora'].values():
        corpus['bleu'] = run_bleu(ref_fns, corpus['tmpfile'])
