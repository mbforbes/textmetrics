"""
Wrapper around METEOR.
"""

# builtins
import code
import subprocess

# local
from textmetrics.common import References, Candidates, METEORResults


def run_meteor(reference_fn: str, candidate_fn: str,
               jar_fn: str = 'textmetrics/meteor/meteor-1.5.jar') -> METEORResults:
    res = subprocess.run(
        ['java', '-Xmx2G', '-jar', jar_fn, candidate_fn, reference_fn, '-l',
        'en', '-norm', '-q'],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    return {
        'overall': float(str(res.stdout.strip())[2:-1])
    }


def meteor(references: References, candidates: Candidates) -> None:
    # easiest mode to run only allows one reference; can add support for more
    # by interleving files in the future if we want it (I think).
    if len(references['corpora']) > 1:
        print('WARNING: METEOR currently only supported for 1 reference')
        return

    # get ref
    rCorpus = list(references['corpora'].values())[0]

    # run meteor for each of the candidates separately
    for cCorpus in candidates['corpora'].values():
        cCorpus['meteor'] = run_meteor(rCorpus['tmpfile'], cCorpus['tmpfile'])
