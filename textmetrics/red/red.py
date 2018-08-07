"""
Simply wraps rouge's API.

(Called "red" to avoid conflicting module names in Python's imports.)
"""

# builtins
import code

# 3rd party
import rouge

# local
from textmetrics.common import References, Candidates, ROUGEResults


def run_red(reference_fn: str, candidate_fn: str) -> ROUGEResults:
    r = rouge.FilesRouge(candidate_fn, reference_fn)
    scores = r.get_scores(avg=True)

    return {
        'rouge1': {
            'precision': scores['rouge-1']['p'],
            'recall': scores['rouge-1']['r'],
            'f1': scores['rouge-1']['f'],
        },
        'rouge2': {
            'precision': scores['rouge-2']['p'],
            'recall': scores['rouge-2']['r'],
            'f1': scores['rouge-2']['f'],
        },
        'rougeL': {
            'precision': scores['rouge-l']['p'],
            'recall': scores['rouge-l']['r'],
            'f1': scores['rouge-l']['f'],
        },
    }


def red(references: References, candidates: Candidates) -> None:
    # reimplementation we're using only allows one reference.
    if len(references['corpora']) > 1:
        print('WARNING: ROUGE currently only supported for 1 reference')
        return

    # get ref
    rCorpus = list(references['corpora'].values())[0]

    # run rouge for each of the candidates separately
    for cCorpus in candidates['corpora'].values():
        cCorpus['rouge'] = run_red(rCorpus['tmpfile'], cCorpus['tmpfile'])
