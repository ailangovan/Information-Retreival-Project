import math

def tfidf(query, index, term_doc_freqs, doc_lengths):
    '''
    Scores documents based on TFIDF from the heuristic modified version
    '''
    doc_score_index = {}
    N = len(doc_lengths)

    for doc in doc_lengths:
        doc_score_num = 0
        doc_score_denom = 0
        for qi in query:

            try:
                doc_freq = float(term_doc_freqs[qi])
            except:
                doc_freq = 0.0

            try:
                inverted_list = index[qi]
                term_freq = float(inverted_list[doc])
            except:
                term_freq = 0.0

            num = float(tfidf_num(float(term_freq) + 0.01, float(doc_freq) + 0.01, N))
            doc_score_num += num
            doc_score_denom += math.pow(num,2)

        doc_score_denom = math.sqrt(doc_score_denom)

        doc_score_index[doc] = doc_score_num/doc_score_denom

    return doc_score_index

def tfidf_num(tf, df, N):
    return (math.log(tf) + 1) * math.log(N/df)
