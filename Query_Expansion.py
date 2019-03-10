from FileUtilities import *
from Scoring_Functions import *
from operator import itemgetter
import math

resultingDS = recreateIndexFromTextFile("unigram_frequency.txt")
index = resultingDS[0]
term_doc_freqs = resultingDS[1]
doc_lengths = docSizes('Doc_Term_Counts.txt')
queries = recreate_queries(True)
stopwords = get_stopword_set()

alpha = 8
beta = 16
gamma = 4

def query_expansion(query_id, query):
    '''
    Uses Rocchio's algorithm to expand a query based on pseudo relevance feedback from
    an initial BM25 retrieval run
    '''
    word_vect = {}
    for term in query:
        if word_vect.get(term):
            word_vect[term] += 1
        else:
            word_vect[term] = 1
    rel_scores = {}

    results = bm25(query, query_id, index, term_doc_freqs, doc_lengths)
    results = sorted(results.items(), key=itemgetter(1), reverse=True)
    relevant_set = set([item[0] for item in results[:20]])

    N = len(doc_lengths)
    inverse_rel = 1/len(relevant_set)
    inverse_non = 1/(len(results) - len(relevant_set))

    for token in index:
        if token not in stopwords:
            idf = math.log(float(N) / float(term_doc_freqs[token]))
            rel_scores[token] = 0
            for doc in index[token]:
                if doc in relevant_set:
                    rel_scores[token] += beta*idf*inverse_rel*float(index[token][doc])
                else:
                    rel_scores[token] -= gamma * idf * inverse_non * float(index[token][doc])

            if word_vect.get(token):
                word_vect[token] = alpha * word_vect[token] \
                                + rel_scores[token]
            else:
                # If a token did not appear in a relevant document, or was barely present, it's score will be at or below zero.
                if rel_scores[token] > 0.0:
                    word_vect[token] = rel_scores[token]

    output = sorted(word_vect.items(), key=itemgetter(1), reverse=True)

    i = 0
    for tuple in output:
        if i == 21:
            break
        if tuple[0] not in query:
            query.append(tuple[0])
            i += 1

    results = bm25(query, query_id, index, term_doc_freqs, doc_lengths)
    outputTop_qe(100, '_'.join(query), results, 'bm25', query_id, False)
    return

def main():
    for query_id, query in queries.items():
        query_expansion(query_id, query)



if __name__ == '__main__':
    main()

