"""
Saves preprocessed text so external scorers can operate on files.

BLEU and METEOR are flexible about where things are located, but ROUGE is more
strict, so we follow rouge conventions.
"""

# builtins
import code
import shutil
import os
import tempfile
from typing import Optional

# local
from textmetrics.common import References, Candidates

# LOL!
REF_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def save(references: Optional[References], candidates: Candidates) -> None:
    # ROUGE has the strictest requirements for how things are laid out, so
    # we're using their scheme for saving the temporary files.
    #
    # Model (reference) directory:
    # - reference.A.001.txt  (ref 1)
    # - reference.B.001.txt  (ref 2)
    # - ...
    # - reference.N.001.txt  (ref N)
    #
    # System (candidate) 1 directory:
    # - candidate.001.txt
    #
    # System (candidate) 2 directory:
    # - candidate.001.txt
    #
    # ...
    #
    # System (candidate) M directory:
    # - candidate.001.txt

    # save candidates. Each lives in its own dir and gets a single file.
    for cCorpus in candidates['corpora'].values():
        cCorpus['tmpdir'] = tempfile.mkdtemp()
        cCorpus['tmpfile'] = os.path.join(
            cCorpus['tmpdir'], 'candidate.001.txt')
        with open(cCorpus['tmpfile'], 'w') as f:
            f.write(cCorpus['contents'])

    # save references if they exist
    if references is None:
        return
    references['tmpdir'] = tempfile.mkdtemp()
    for i, rCorpus in enumerate(references['corpora'].values()):
        rCorpus['tmpfile'] = os.path.join(  # type: ignore
            references['tmpdir'],
            'reference.{}.001.txt'.format(REF_LABELS[i])
        )
        with open(rCorpus['tmpfile'], 'w') as f:
            f.write(rCorpus['contents'])


def cleanup(references: Optional[References], candidates: Candidates) -> None:
    # cleanup candidates' tmp files
    for cCorpus in candidates['corpora'].values():
        shutil.rmtree(cCorpus['tmpdir'])

    # cleanup references' tmp files if they exist
    if references is None or references['tmpdir'] is None:
        return
    shutil.rmtree(references['tmpdir'])

