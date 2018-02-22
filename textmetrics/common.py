"""
Types!
"""

# builtins
from typing import Dict, List, Optional, Union

# 3rd party
from mypy_extensions import TypedDict

# results from auto comparative metric systems

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


class METEORResults(TypedDict):
    overall: float


# results from custom intrinsic metrics

class NgramResults(TypedDict):
    # maps ngram number to number of unique ngram of that n
    gram: Dict[int, int]


# corpora objects. reference corpora are fairly barebones. candidate corpora
# are off in their own directory as well, and store the results of their auto
# eval metrics.

class Corpus(TypedDict):
    contents: str


class ReferenceCorpus(Corpus, total=False):
    tmpfile: str


class CandidateCorpus(Corpus, total=False):
    tmpfile: str
    tmpdir: str
    bleu: BLEUResults
    rouge: ROUGEResults
    meteor: METEORResults
    ngrams: NgramResults


# references and candidates are the bigger objects that we pass around.

class References(TypedDict):
    corpora: Dict[str, ReferenceCorpus]
    tmpdir: Optional[str]

class Candidates(TypedDict):
    corpora: Dict[str, CandidateCorpus]
