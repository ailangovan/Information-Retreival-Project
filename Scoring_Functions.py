import subprocess
from bm25 import bm25
from jmsmoothing import jm_smoothing
from tfidf import tfidf
from bs4 import BeautifulSoup, NavigableString
from Tokenizer import Tokenize_String
from FileUtilities import *
from SnippetGeneration import *

def recreate_queries(stopping):
    '''
    Pulls the queries into memory for executing retrieval of documents.
    If stopping is true, remove stopwords from the query.
    '''
    f = open('cacm.query.txt','r')
    r = f.read()
    soup = BeautifulSoup(r, 'html5lib')
    docs = soup.find_all('doc')

    output = {}

    if stopping:
        stopwords = get_stopword_set()

    for doc in docs:
        doc_id = doc.find('docno').get_text().strip()
        text = ''.join([element for element in doc if isinstance(element, NavigableString)]).strip().replace('\n',' ')
        text = Tokenize_String(text)
        if stopping:
            text = remove_stopwords(text, stopwords)
        output[doc_id] = text

    return output

def run_scoring_functions(index, term_doc_freqs, doc_lengths, queries, function_type, stopping, generateSnippet):
    '''
    Runs a given scoring method and outputs the top 100 ranked documents
    '''
    for key,value in queries.items(): # key, value is qNum: [queryToken, ..., queryToken]
        if function_type == 'jmsmoothing':
            results = jm_smoothing(value, index, doc_lengths, 0.35)
        elif function_type == 'bm25':
            results = bm25(value, key, index, term_doc_freqs, doc_lengths)
        elif function_type == 'tfidf':
            results = tfidf(value, index, term_doc_freqs, doc_lengths)
        outputTop(100, '_'.join(value), results, function_type, key, stopping)
        if generateSnippet:
            top100Documents = []
            # should refactor this above results going into top100 so we don't do this twice.
            sortedResults = sorted(results.items(), key = itemgetter(1), reverse = True)
            for i in range(0, 100):
                top100Documents.append(sortedResults[i][0])
            snippets = snippetGenerator(top100Documents, value, 5, key)
            outputSnippet('_'.join(value), snippets, function_type, key, stopping)

def remove_stopwords(query_tokens, stopwords):
    '''
    Removes stopwords from a token set
    '''
    output = []
    for token in query_tokens:
        if token in stopwords:
            continue

        output.append(token)
    return output

def get_stopword_set():
    '''
    Retrieves the stopword set from the given text file
    '''
    f = open('common_words','r')
    words = f.read().splitlines()
    return set(words)
