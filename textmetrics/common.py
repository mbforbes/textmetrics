"""
Types!
"""

# builtins
from typing import Dict, List, Optional, Union

# 3rd party
from mypy_extensions import TypedDict

class BLEUResults(TypedDict):
    overall: float
    bleu1: float
    bleu2: float
    bleu3: float
    bleu4: float
    brevity_penalty: float
    length_ratio: float
    candidate_length: int
    reference_length: int

class Corpus(TypedDict):
    contents: str
    tmpfile: Optional[str]

class CandidateCorpus(Corpus, total=False):
    bleu: BLEUResults

Corpora = Dict[str, Corpus]
CandidateCorpora = Dict[str, CandidateCorpus]

Worklist = List[Union[Corpora, CandidateCorpora]]
