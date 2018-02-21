"""
Runs text metrics.
"""

# builtins
import argparse
import code
import os
import tempfile
from typing import Dict, Optional, List, Any

# 3rd party
from mypy_extensions import TypedDict
from tabulate import tabulate

# local
from bleu import bleu
from common import Worklist, Corpora, CandidateCorpora, CandidateCorpus
from preprocess import clean


def display_results(candidates: CandidateCorpora) -> None:
    # Desired format:
    #
    # res type      candidate1      candidate 2      ...
    # ---             ----             ----
    # res1           c1/r1             c2/r1
    # res2           c1/r2             c2/r2
    # ...            ...                ...
    # resn           c1/rn             c2/rn
    #

    # making a list of candidates so we can consistently iterate over them
    c_keys = list(candidates.keys())
    header = ['Score'] + [os.path.basename(k) for k in c_keys]

    # build
    rows: List[List[Any]] = []
    # row_info contains the row name, a tester function to see if the candidate
    # has the datum, and an extractor function to extract the value from the
    # candidate if so
    row_info = [
        ('BLEU: Overall', lambda x: 'bleu' in x and 'overall' in x['bleu'], lambda x: x['bleu']['overall']),
        ('BLEU-1', lambda x: 'bleu' in x and 'bleu1' in x['bleu'], lambda x: x['bleu']['bleu1']),
        ('BLEU-2', lambda x: 'bleu' in x and 'bleu2' in x['bleu'], lambda x: x['bleu']['bleu2']),
        ('BLEU-3', lambda x: 'bleu' in x and 'bleu3' in x['bleu'], lambda x: x['bleu']['bleu3']),
        ('BLEU-4', lambda x: 'bleu' in x and 'bleu4' in x['bleu'], lambda x: x['bleu']['bleu4']),
    ]
    for row_name, tester, extractor in row_info:
        row = [row_name]
        for c_key in c_keys:
            candidate = candidates[c_key]
            if tester(candidate):
                row.append(extractor(candidate))
            else:
                row.append('--')
        rows.append(row)

    # display
    print(tabulate(rows, headers=header))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--clean-tokens',
        type=argparse.FileType('r'),
        default='textmetrics/preprocess/clean_tokens.txt',
        help='file to read tokens to remove (one perline)')
    parser.add_argument(
        '--references',
        nargs='+',
        type=argparse.FileType('r'),
        help='list of reference files (needed for comparative metrics)')
    parser.add_argument(
        'candidates',
        nargs='+',
        type=argparse.FileType('r'),
        help='list of candidate files')
    args = parser.parse_args()

    # Read files in to do preprocessing
    print('INFO: Reading files...')
    references: Optional[Corpora]
    candidates: CandidateCorpora
    references = {r.name: {'contents': r.read(), 'tmpfile': None}
        for r in args.references} if args.references is not None else None
    candidates = {c.name: {
        'contents': c.read(),
        'tmpfile': None,
        'bleu': None,
        } for c in args.candidates}

    # TODO: include tokenization at some point

    # Preprocessing: Token removal
    print('INFO: Preprocessing: Removing extraneous tokens...')
    removal = clean.load(args.clean_tokens)
    worklist: Worklist
    worklist = [candidates, references] if references is not None else [candidates]
    for d in worklist:
        for val in d.values():
            val['contents'] = clean.clean(val['contents'], removal)

    # Comparative metrics
    if references is not None:
        # BLEU
        print('INFO: Computing BLEU...')
        bleu.bleu(references, candidates)

    # Display
    print('INFO: Formatting results...')
    display_results(candidates)


if __name__ == '__main__':
    main()
