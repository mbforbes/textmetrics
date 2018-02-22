"""
Types!
"""

# builtins
from typing import Dict, List, Optional, Union

# 3rd party
from mypy_extensions import TypedDict

# results from auto metric systems

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


class PRF(TypedDict):
    precision: float
    recall: float
    f1: float


class ROUGEResults(TypedDict):
    rouge1: PRF
    rouge2: PRF
    rougeL: PRF


# corpora objects. reference corpora are fairly barebones. candidate corpora
# are off in their own directory as well, and store the results of their auto
# eval metrics.

class Corpus(TypedDict):
    contents: str
    tmpfile: Optional[str]


class ReferenceCorpus(Corpus):
    pass


class CandidateCorpus(Corpus, total=False):
    tmpdir: Optional[str]
    bleu: BLEUResults
    rouge: ROUGEResults


# references and candidates are the bigger objects that we pass around.

class References(TypedDict):
    corpora: Dict[str, ReferenceCorpus]
    tmpdir: Optional[str]

class Candidates(TypedDict):
    corpora: Dict[str, CandidateCorpus]
