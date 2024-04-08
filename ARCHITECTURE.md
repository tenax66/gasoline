# ARCHITECTURE

# BM25

The BM25 score of a document D for a given query Q is:

$$\text{score}(D,Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

where $q_1, q_2, \dots, q_n$ are the keywords in $Q$, and $f(q_i, D)$ is the number of times that the keyword $q_i$ occurs in the document D.  
$|D|$ is the length of the document D in words, and $\text{avgdl}$ is the average document length of the text collection from which documents are extracted.

$k_1$ and $b$ are free parameters, and they are typically chosen as $k_1\in[1.2, 2.0]$ and $b=0.75$.

$\text{IDF}(q_i)$ is the IDF ([inverse document frequency](https://en.wikipedia.org/wiki/Inverse_document_frequency)) of the $q_i$.

$$\text{IDF}(q_i) = \ln \left(\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5}+1\right)$$

where $N$ is the total number of documents in the corpus, and $n(q_{i})$ is the number of documents containing q(i).
