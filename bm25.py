import math

def countQ(q, queryList):
    """
    Reports the frequency of q in the query
    """
    count = 0
    for token in queryList:
        if q == token:
            count += 1
    return count

def bm25(query, qNum, invertedIndex, term_doc_freqs, doc_lengths):
    """
    Calculates the BM25 score.
    """
    doc_score_index = {}
    k1 = 1.2
    k2 = 500
    b = 0.75
    avdl = get_average_doc_len(doc_lengths)
    for doc in doc_lengths:
        doc_score = 0.0
        D = float(doc_lengths[doc])
        K = bm25_K(b, k1, D, avdl)
        N = float(len(doc_lengths))
        for q in query:
            try:
                n = float(term_doc_freqs[q])
            except:
                n = 0

            try:
               f = float(invertedIndex[q][doc])
            except:
                f = 0

            qf = countQ(q, query) # counts the number of times q is in the query

            doc_score += (first_part(n, N) * second_part(k1, K, f) * third_part(k2, qf))
        doc_score_index[doc] = doc_score
    return doc_score_index

def first_part(n, N):
    """
    Helper Function to the BM25 score. It's a subcomponent
    of the BM25 equation.
    """
    return math.log(1/((n + 0.5)/(N - n + 0.5)))

def second_part(k1, K, f):
    """
    Helper Function to the BM25 Score
    It's a subcomponent of the BM25 equation.
    """
    return ((k1 + 1)*f/(K + f))

def third_part(k2, qf):
    """
    Helper Function to the BM25 Score
    It's a subcomponent of the BM25 equation.
    """
    return ((k2+1)*qf / (k2 + qf))

def bm25_K(b, k1, dl, avdl):
    """ 
    Calculates the K value to be used in the BM25 function
    """
    return k1 * ((1 - b) + (b * (dl / avdl)))


def get_average_doc_len(doc_lengths):
    """
    Returns the average document length for the entire corpus
    """
    total_word_occurrences = 0
    for doc in doc_lengths:
        total_word_occurrences += float(doc_lengths[doc])

    return float(total_word_occurrences / len(doc_lengths))