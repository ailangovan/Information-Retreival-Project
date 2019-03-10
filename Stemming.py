import re
import os
from FileUtilities import recreateIndexFromTextFile, docSizes
from bm25 import bm25
from jmsmoothing import jm_smoothing
from tfidf import tfidf
from operator import itemgetter

def Stemming_Output_Top100(numberToOutput, query, results, scoringMethod, query_number):
    """ Outputs the top (e.g. 100) ranked scores to a fileName for a list of queries"""
    basePath = os.getcwd()
    # filename = [scoring method_query_number.txt]
    filename = scoringMethod+'_'+str(query_number)
    filename += '_stemmed'
    filename += '.txt'
    filePath = "%s/Outputs/%s" % (basePath, filename)
    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print("File path incorrect or does not exist")
    output = open(filePath, 'w')
    rank = 0
    results = sorted(results.items(), key = itemgetter(1), reverse = True)
    for doc in results:
        # print ("dc", doc)
        if rank < 100:
            rank = rank + 1
            line = "%s Q0 %s %d %s %s\n" % (query, doc[0], rank, doc[1], scoringMethod )
            output.write(line)
    output.close()

def Stemming_run_scoring_functions():
    '''
    Executes all three retrieval methods on the stemmed corpus for the set of stemmed queries
    '''
    resultingDS = recreateIndexFromTextFile("unigram_stem_frequency.txt")
    index = resultingDS[0]
    term_doc_freqs = resultingDS[1]
    doc_lengths = docSizes('Doc_Term_Counts_Stem.txt')
    queries = recreate_queries_T3B()
    i = 1
    for query in queries:
        query = query.split()
        results = jm_smoothing(query, index, doc_lengths, 0.35)
        Stemming_Output_Top100(100, '_'.join(query), results, 'jmsmoothing', i)

        results = bm25(query, i, index, term_doc_freqs, doc_lengths)
        Stemming_Output_Top100(100, '_'.join(query), results, 'bm25', i)

        results = tfidf(query, index, term_doc_freqs, doc_lengths)
        Stemming_Output_Top100(100, '_'.join(query), results, 'tfidf', i)

        i+=1

def recreate_queries_T3B():
    '''
    Retrieves the stemmed queries from the text file
    '''
    f = open('cacm_stem.query.txt','r')
    lines = f.read().splitlines()
    return lines

def Stemming_Tokenizer():
    '''
    Tokenizes the stemmed corpus
    '''
    start_new_doc = "# [0-9]"
    pattern = re.compile(start_new_doc)
    f = open('cacm_stem.txt','r')
    lines = f.read().splitlines()

    reading_text = False
    current_doc = ''

    tokens = {}

    for line in lines:
        if reading_text:
            s = line.split()

            for str in s:
                if str == 'pm' or str == 'am':
                    tokens[current_doc].append(str)
                    reading_text = False
                    break
                else:
                    tokens[current_doc].append(str)
        elif pattern.match(line) is not None:
            s = line.split()
            tokens[s[1]] = []
            current_doc = s[1]
            reading_text = True

    return tokens

# Stores a term index for an inverted index
class Term:
    def __init__(self, term):
        self.term = term
        self.list_length = 0
        self.inverted_list = []

    def add_entry(self, entry):
        self.list_length += 1
        self.inverted_list.append(entry)

# merge a document's partial index into the main index
def merge_partial_index(main_index, partial_index, doc_id):
    for term in partial_index:
        if main_index.get(term):
            main_index[term].add_entry((doc_id, partial_index[term]))
        else:
            main_index[term] = Term(term)
            main_index[term].add_entry((doc_id, partial_index[term]))

# output function
def write_index_to_file(index, ngram, type):
    f = open(ngram + '_' + type + '.txt', 'w+')
    for term in index:
        f.write(term + ',\t' + str(index[term].list_length) + ',\t')
        for entry in index[term].inverted_list:
            f.write(entry[0] + ':' + str(entry[1]) + '\t')
        f.write('\n')
    f.close()

def Stemming_Indexer(token_dict):
    '''
    Indexes the stemmed corpus
    '''

    # master indexes and document_term_count data structures
    unigram_index_tf = {}
    doc_term_counts = {}

    # create a partial index for each document in the corpus, then merge into the main index
    for file in token_dict:
        tokens = token_dict[file]
        unigram_freqs = {}
        number_unigrams = 0

        for i in range(0, len(tokens)):
            if not unigram_freqs.get(tokens[i]):
                unigram_freqs[tokens[i]] = 1

            else:
                unigram_freqs[tokens[i]] += 1
            number_unigrams += 1

        doc_term_counts[file] = number_unigrams

        merge_partial_index(unigram_index_tf, unigram_freqs, file)

        write_index_to_file(unigram_index_tf, 'unigram_stem', 'frequency')

        f = open('Doc_Term_Counts_Stem.txt', 'w+')
        for did in doc_term_counts:
            terms = doc_term_counts[did]
            f.write(did + ' unigrams: ' + str(terms) + '\n')
        f.close()

def Stemming():
    tokens = Stemming_Tokenizer()
    Stemming_Indexer(tokens)

    Stemming_run_scoring_functions()
