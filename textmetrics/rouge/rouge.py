"""
Simply wraps pyrouge's API.
"""

# 3rd party
import code
from pyrouge import Rouge155

# local
from common import References, Candidates, ROUGEResults


def runrouge(reference_dir: str, reference_pattern: str,
             candidate_dir: str, candidate_pattern: str) -> ROUGEResults:
    # TODO: should this be a global so it's only init'd once?
    r = Rouge155()

    # setup references ("model" in ROUGE lingo)
    r.model_dir = reference_dir
    r.model_filename_pattern = reference_pattern

    # setup candidate ("system" in ROUGE lingo)
    r.system_dir = candidate_dir
    r.system_filename_pattern = candidate_pattern

    # TODO: consider adding this
    # r.split_sentences()

    # run and convert
    output = r.convert_and_evaluate()
    output_dict = r.output_to_dict(output)
    # print(output)
    # print(output_dict)

    # NOTE: the above rouge either has a bug in the wrapper, or it's so slow it
    # doesn't finish a single file in 10 minutes. I'm going to switch to a
    # reimplementation.

    return {
        'overall': 0.0,
    }


def rouge(references: References, candidates: Candidates) -> None:
    # run rouge for each of the candidates separately
    for cCorpus in candidates['corpora'].values():
        cCorpus['rouge'] = runrouge(
            references['tmpdir'],
            'reference.[A-Z].#ID#.txt',
            cCorpus['tmpdir'],
            'candidate.(\d+).txt')
