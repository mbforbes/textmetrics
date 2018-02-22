"""
Runs text metrics.
"""

# builtins
import argparse
import code
import os
import sys
import tempfile
from typing import Dict, Optional, List, Any

# 3rd party
from mypy_extensions import TypedDict
from tabulate import tabulate

# local
from bleu import bleu
from rouge import rouge
from common import Corpus, Candidates, References
from utility import clean, storage


def display_results(candidates: Candidates) -> None:
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
    c_keys = list(candidates['corpora'].keys())
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
            candidate = candidates['corpora'][c_key]
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
        default='textmetrics/utility/clean_tokens.txt',
        help='file to read tokens to remove (one perline)')
    parser.add_argument(
        '--references',
        nargs='+',
        type=argparse.FileType('r'),
        help='list of reference files (needed for comparative metrics) (max 26)')
    parser.add_argument(
        'candidates',
        nargs='+',
        type=argparse.FileType('r'),
        help='list of candidate files')
    args = parser.parse_args()

    # LOL!
    if args.references is not None and len(args.references) > 26:
        print('ERROR: Can only have at most 26 references. If you really need')
        print('ERROR: more than this, modify the code.')
        sys.exit(1)

    # Read files in to do preprocessing
    print('INFO: Reading files...')
    references: Optional[References] = None
    if args.references is not None:
        references = {
            'corpora': {
                r.name: {
                    'contents': r.read(),
                    'tmpfile': None
                } for r in args.references
            },
            'tmpdir': None,
        }

    candidates: Candidates = {
        'corpora': {
            c.name: {
                'contents': c.read(),
                'tmpfile': None,
                'tmpdir': None,
                'bleu': None,
            } for c in args.candidates
        },
    }

    # TODO: include tokenization at some point

    # Preprocessing: Token removal
    print('INFO: Preprocessing: Removing extraneous tokens...')
    removal = clean.load(args.clean_tokens)
    worklist: List[Corpus] = list(candidates['corpora'].values())
    if references is not None:
        worklist += list(references['corpora'].values())  # type: ignore
    for corpus in worklist:
        corpus['contents'] = clean.clean(corpus['contents'], removal)

    # Storage
    print('INFO: Preprocessing: Storing temporary files...')
    storage.save(references, candidates)

    # Comparative metrics
    if references is not None:
        # BLEU
        print('INFO: Computing BLEU...')
        bleu.bleu(references, candidates)

        # BLEU
        print('INFO: Computing ROUGE...')
        rouge.rouge(references, candidates)

    # Cleanup
    print('INFO: Postprocessing: Removing temporary files...')
    storage.cleanup(references, candidates)

    # Display
    print('INFO: Formatting results...')
    display_results(candidates)


if __name__ == '__main__':
    main()
