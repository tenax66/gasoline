from collections import defaultdict
import string


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
    def __init__(self):
        self._index: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        """
        A mapping that, given a word: str, returns another mapping from URL: str
        to the number of times the word appears in the URL: int.
        """

        self._documents: dict[str, str] = {}

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
