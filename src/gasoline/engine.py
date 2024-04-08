from collections import defaultdict
from math import log
import string


def update_url_scores(existing: dict[str, float], new: dict[str, float]):
    for url, score in new.items():
        if url in existing:
            existing[url] += score
        else:
            existing[url] = score
    return existing


def normalize_string(input_string: str) -> str:
    """Normalizes input string. (e.g. remove punctuation, everything to lowercase, etc.)

    Parameters
    ----------
    input_string: str

    Returns
    -------
    str
    """
    translation_table = str.maketrans(string.punctuation, " " * len(string.punctuation))
    string_without_punc = input_string.translate(translation_table)
    string_without_double_spaces = " ".join(string_without_punc.split())
    return string_without_double_spaces.lower()


class SearchEngine:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self._index: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        """
        A mapping that, given a word: str, returns another mapping from URL: str
        to the number of times the word appears in the URL: int.
        """

        self._documents: dict[str, str] = {}

        self.k1 = k1
        """the free parameter of BM25"""
        self.b = b
        """the free parameter of BM25"""

    @property
    def posts(self) -> list[str]:
        return list(self._documents.keys())

    @property
    def number_of_documents(self) -> int:
        return len(self._documents)

    @property
    def avgdl(self) -> float:
        return sum(len(d) for d in self._documents.values()) / len(self._documents)

    def search(self, query: str) -> dict[str, float]:
        keywords = normalize_string(query).split(" ")
        url_scores: dict[str, float] = {}
        for kw in keywords:
            kw_urls_score = self.bm25(kw)
            url_scores = update_url_scores(url_scores, kw_urls_score)
        return url_scores

    def idf(self, keyword: str) -> float:
        """Computes inverse document frequency for a given keyword.

        Parameters
        ----------
        kw: str
            keyword for IDF.
        """
        N = self.number_of_documents
        n_kw = len(self.get_urls(keyword))
        return log((N - n_kw + 0.5) / (n_kw + 0.5) + 1)

    def bm25(self, kw: str) -> dict[str, float]:
        """For all the indexed documents, returns the BM25 score for the keyword.

        Parameters
        ----------
        kw: str
            keyword for calculating the bm25 score.

        Returns
        -------
        dict[str, float]
            mapping from all the URLs that contain the keyword given to their score.
        """
        result = {}
        idf_score = self.idf(kw)
        avgdl = self.avgdl
        for url, freq in self.get_urls(kw).items():
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (
                1 - self.b + self.b * len(self._documents[url]) / avgdl
            )
            result[url] = idf_score * numerator / denominator
        return result

    def index(self, url: str, content: str) -> None:
        """Add an URL and its content to the index.

        Parameters
        ----------
        url: str
        content: str
        """
        self._documents[url] = content
        words = normalize_string(content).split(" ")
        for word in words:
            self._index[word][url] += 1

    def bulk_index(self, documents: list[tuple[str, str]]) -> None:
        for url, content in documents:
            self.index(url, content)

    def get_urls(self, keyword: str) -> dict[str, int]:
        """Returns the URLs that contain the keyword given.

        Parameters
        ----------
        url: str
        content: str
        """
        keyword = normalize_string(keyword)
        return self._index[keyword]


engine = SearchEngine()
