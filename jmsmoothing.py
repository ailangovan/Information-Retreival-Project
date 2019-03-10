import math

def jm_smoothing(query, invertedIndex, doc_lengths, lmbd):
    """
    Executes JM Smoothing scoring for a given query on the full set of documents
    """
    doc_score_index = {}
    collection_total = get_collection_total(doc_lengths)
    one_minus_lambda = 1 - lmbd

    for doc in doc_lengths:
        D = float(doc_lengths[doc])
        doc_score = 0.0
        for qi in query:
            collection_freq = 0
            doc_frequency = 0
            if qi in invertedIndex:
                for i in invertedIndex[qi]:
                    if i == doc:
                        doc_frequency = float(invertedIndex[qi][i])
                    collection_freq += float(invertedIndex[qi][i])
                doc_score = doc_score + math.log(one_minus_lambda*(doc_frequency/D) + lmbd*(collection_freq/collection_total))
        doc_score_index[doc] = doc_score
    return doc_score_index




def get_collection_total(dfs):
    """
    Returns the Corpus Size
    """
    total_count = 0
    for doc in dfs.keys():
        total_count += float(dfs[doc])
    return total_count