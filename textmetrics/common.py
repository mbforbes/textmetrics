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
    # each maps ngram number to average: unique ngrams per line, total ngrams
    # per line (i.e., average line length), ratio of unique to total per line
    # (i.e., some approximation of repetition).
    perline_avg_unique: Dict[int, float]
    perline_avg_total: Dict[int, float]
    perline_avg_ratio: Dict[int, float]

    # each maps ngram number to overall stats: unique ngrams (i.e., ngram
    # vocab), total ngrams (e.g., n=1 means length), ratio of unique ngrams /
    # total ngrams (i.e., some approximation of diversity of outputs).
    overall_unique: Dict[int, int]
    overall_total: Dict[int, int]
    overall_ratio: Dict[int, float]


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
