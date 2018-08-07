"""
Runs text metrics.
"""

# builtins
import argparse
import code
from enum import Enum, auto
import os
import sys
import tempfile
from typing import Dict, Optional, List, Any, Union, Tuple

# 3rd party
from mypy_extensions import TypedDict
from tabulate import tabulate

# local
from textmetrics.bleu import bleu
from textmetrics.common import Corpus, CandidateCorpus, Candidates, References
from textmetrics.custom import ngrams
from textmetrics.meteor import meteor
from textmetrics.red import red
from textmetrics.utility import clean, storage


# class Metric(Enum):
#     COMPARATIVE = auto()
#     INTRINSIC = auto()

class Verbosity(object):
    SUMMARY = 0
    DETAIL = 1


Cell = Union[str,int,float]
MetricWorklist = List[Tuple[int, str, List[Any]]]

def k(c: CandidateCorpus, keys: List[Union[str,int]],
      default: str = '--') -> Cell:
    """Retrieves value of `c` indexed by `keys` (list of keys to be applied),
    or `default` if not found.
    """
    cur = c
    for k in keys:
        if cur is None or k not in cur:
            return default
        cur = cur[k]  # type: ignore
    return cur  # type: ignore


def display_results(
        candidates: Candidates,
        comparative: bool = True,
        intrinsic: bool = True,
        verbosity: int = Verbosity.DETAIL) -> None:
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
    header = ['Metric'] + [os.path.basename(k) for k in c_keys]

    # row_info contains the row name, a tester function to see if the candidate
    # has the datum, and an extractor function to extract the value from the
    # candidate if so
    comp_rows: MetricWorklist = [
        (Verbosity.SUMMARY, 'BLEU: Overall', ['bleu', 'overall']),
        (Verbosity.DETAIL, 'BLEU-1', ['bleu', 'bleu1']),
        (Verbosity.DETAIL, 'BLEU-2', ['bleu', 'bleu2']),
        (Verbosity.DETAIL, 'BLEU-3', ['bleu', 'bleu3']),
        (Verbosity.DETAIL, 'BLEU-4', ['bleu', 'bleu4']),
        (Verbosity.DETAIL, 'BLEU: brevity penalty', ['bleu', 'brevity_penalty']),
        (Verbosity.DETAIL, 'BLEU: length ratio', ['bleu', 'length_ratio']),
        (Verbosity.DETAIL, 'BLEU: candidate len', ['bleu', 'candidate_length']),
        (Verbosity.DETAIL, 'ROUGE-L: Precision', ['rouge', 'rougeL', 'precision']),
        (Verbosity.DETAIL, 'ROUGE-L: Recall', ['rouge', 'rougeL', 'recall']),
        (Verbosity.SUMMARY, 'ROUGE-L: F1', ['rouge', 'rougeL', 'f1']),
        (Verbosity.SUMMARY, 'METEOR', ['meteor', 'overall']),
    ]
    intr_rows: MetricWorklist = [
        # overall
        (Verbosity.SUMMARY, '1-grams: overall unique (vocab)', ['ngrams', 'overall_unique', 1]),
        (Verbosity.SUMMARY, '1-grams: overall total (len)', ['ngrams', 'overall_total', 1]),
        (Verbosity.SUMMARY, '1-grams: overall ratio (unique/total)', ['ngrams', 'overall_ratio', 1]),
        (Verbosity.DETAIL, '2-grams: overall unique', ['ngrams', 'overall_unique', 2]),
        (Verbosity.DETAIL, '2-grams: overall total', ['ngrams', 'overall_total', 2]),
        (Verbosity.DETAIL, '2-grams: overall ratio (unique/total)', ['ngrams', 'overall_ratio', 2]),
        (Verbosity.DETAIL, '3-grams: overall unique', ['ngrams', 'overall_unique', 3]),
        (Verbosity.DETAIL, '3-grams: overall total', ['ngrams', 'overall_total', 3]),
        (Verbosity.DETAIL, '3-grams: overall ratio (unique/total)', ['ngrams', 'overall_ratio', 3]),
        (Verbosity.DETAIL, '4-grams: overall unique', ['ngrams', 'overall_unique', 4]),
        (Verbosity.DETAIL, '4-grams: overall total', ['ngrams', 'overall_total', 4]),
        (Verbosity.DETAIL, '4-grams: overall ratio (unique/total)', ['ngrams', 'overall_ratio', 4]),

        # per-line
        (Verbosity.SUMMARY, '1-grams: per-line avg unique (line-vocab)', ['ngrams', 'perline_avg_unique', 1]),
        (Verbosity.SUMMARY, '1-grams: per-line avg total (line-len)', ['ngrams', 'perline_avg_total', 1]),
        (Verbosity.SUMMARY, '1-grams: per-line ratio (unique/total)', ['ngrams', 'perline_avg_ratio', 1]),
        (Verbosity.DETAIL, '2-grams: per-line avg unique', ['ngrams', 'perline_avg_unique', 2]),
        (Verbosity.DETAIL, '2-grams: per-line avg total', ['ngrams', 'perline_avg_total', 2]),
        (Verbosity.DETAIL, '2-grams: per-line ratio (unique/total)', ['ngrams', 'perline_avg_ratio', 2]),
        (Verbosity.DETAIL, '3-grams: per-line avg unique', ['ngrams', 'perline_avg_unique', 3]),
        (Verbosity.DETAIL, '3-grams: per-line avg total', ['ngrams', 'perline_avg_total', 3]),
        (Verbosity.DETAIL, '3-grams: per-line ratio (unique/total)', ['ngrams', 'perline_avg_ratio', 3]),
        (Verbosity.DETAIL, '4-grams: per-line avg unique', ['ngrams', 'perline_avg_unique', 4]),
        (Verbosity.DETAIL, '4-grams: per-line avg total', ['ngrams', 'perline_avg_total', 4]),
        (Verbosity.DETAIL, '4-grams: per-line ratio (unique/total)', ['ngrams', 'perline_avg_ratio', 4]),
    ]

    # select comparative and intrinsic subsets independently
    worklist: MetricWorklist = []
    if comparative:
        worklist.extend(comp_rows)
    if intrinsic:
        worklist.extend(intr_rows)

    # build
    rows: List[List[Cell]] = []
    for v, name, keys in worklist:
        # only display rows matching desired verbosity
        if v > verbosity:
            continue
        row: List[Cell] = [name]
        for c_key in c_keys:
            row.append(k(candidates['corpora'][c_key], keys))
        rows.append(row)

    # TODO: make display method
    # display csv
    # for row in [header] + rows:
    #     print(','.join([str(cell) for cell in row]))

    # display table
    print(tabulate(rows, headers=header))


def main() -> None:
    parser = argparse.ArgumentParser()
    # optional behavior args
    parser.add_argument(
        '--clean-tokens',
        type=argparse.FileType('r'),
        default=clean.DEFAULT_FILE,
        metavar='PATH',
        help='file to read tokens to remove (one per line) (default: {}'.format(
            clean.DEFAULT_FILE))
    parser.add_argument(
        '--no-comparative',
        action='store_true',
        help='provied to skip comparative metrics (BLEU, ROUGE, METEOR)')
    parser.add_argument(
        '--no-intrinsic',
        action='store_true',
        help='provied to skip intrinsic metrics (ngrams (incl. vocab), sentence lengths)')
    parser.add_argument(
        '--verbosity',
        type=int,
        default=1,
        metavar='N',
        help='how many metrics to display: 0 = summaries only, 1 = all (default)')
    # core args: candidates (required), references (optional)
    parser.add_argument(
        '--references',
        nargs='+',
        type=argparse.FileType('r'),
        metavar='PATH',
        help='list of reference files (needed for comparative metrics) (max 26)')
    parser.add_argument(
        'candidates',
        nargs='+',
        type=argparse.FileType('r'),
        help='list of candidate files')
    args = parser.parse_args()

    print('INFO: Using verbosity: {}'.format(args.verbosity))

    # LOL!
    if args.references is not None and len(args.references) > 26:
        print('ERROR: Can only have at most 26 references. If you really need')
        print('ERROR: more than this, modify the code.')
        sys.exit(1)

    # Read files in to do preprocessing
    print('INFO: Reading files...')
    references: Optional[References] = None
    if args.references is not None and not args.no_comparative:
        references = {
            'corpora': {
                r.name: {
                    'contents': r.read(),
                } for r in args.references
            },
            'tmpdir': None,
        }

    candidates: Candidates = {
        'corpora': {
            c.name: {
                'contents': c.read(),
            } for c in args.candidates
        },
    }

    # TODO: include tokenization at some point

    # Preprocessing: Token removal
    print('INFO: Preprocessing: Removing extraneous tokens...')
    removal = clean.load(args.clean_tokens)
    worklist: List[Corpus] = list(candidates['corpora'].values())
    if references is not None:
        worklist += list(references['corpora'].values())
    for corpus in worklist:
        corpus['contents'] = clean.clean(corpus['contents'], removal)

    # Storage
    print('INFO: Preprocessing: Storing temporary files...')
    storage.save(references, candidates)

    # Comparative metrics
    if args.no_comparative:
        # Explicitly log that we're skipping only if they explicitly asked to
        # skip.
        print('INFO: Skipping comparative metrics...')
    if references is not None:
        # BLEU
        print('INFO: Computing BLEU...')
        bleu.bleu(references, candidates)

        # ROUGE
        print('INFO: Computing ROUGE...')
        red.red(references, candidates)

        # METEOR
        print('INFO: Computing METEOR...')
        meteor.meteor(references, candidates)

    # Intrinsic metrics
    if args.no_intrinsic:
        print('INFO: Skipping intrinsic metrics...')
    else:
        # Ngrams (incl. vocab w/ unigrams)
        print('INFO: Computing ngrams...')
        ngrams.ngrams(candidates)

    # Cleanup
    print('INFO: Postprocessing: Removing temporary files...')
    storage.cleanup(references, candidates)

    # Display
    print('INFO: Formatting results...')
    display_results(
        candidates,
        not args.no_comparative,
        not args.no_intrinsic,
        args.verbosity)


if __name__ == '__main__':
    main()
