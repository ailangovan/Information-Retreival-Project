from Indexer import Indexer
from Tokenizer import Tokenizer
from FileUtilities import recreateIndexFromTextFile, docSizes
from Scoring_Functions import *
from Stemming import Stemming

valid_scoring_methods = ['jmsmoothing', 'bm25', 'tfidf']

def main():
    print('CS6200 Final Project')

    stemming = input('Do you wish to do a stemming run? (y/n): ')

    if stemming.lower() == 'y':
        Stemming()
        exit()

    indexer_input = input('Input the local directory you want to index (q to skip step): ')

    if indexer_input.lower() != 'q':
        print ("Tokenizing")
        tokens = Tokenizer(indexer_input)
        print ("Finished Tokenizing")
        print ("Indexing")
        Indexer(tokens)
        print ("Finished Indexing")

    scoring_method = input("Select scoring method: 'jmsmoothing', 'bm25', 'tfidf': ")

    stopping_query = input("Apply stopping to the query? (y/n): ")

    if stopping_query.lower() == 'n':
        stopping = False
    else:
        stopping = True

    print ("Scoring Documents")
    
    queries = recreate_queries(stopping)
    invertedIndex, term_doc_freqs = recreateIndexFromTextFile("unigram_frequency.txt")
    document_lengths = docSizes('Doc_Term_Counts.txt')

    generateSnippetsInput = input("Would you like to see the snippets? 'n' for no, will otherwise default to yes: ")
    generateSnippet = True
    if generateSnippetsInput == 'n':
        generateSnippet = False

    if scoring_method in valid_scoring_methods:
        run_scoring_functions(invertedIndex, term_doc_freqs, document_lengths, queries, scoring_method, stopping, generateSnippet)
    else:
        raise Exception('Bad Scoring Method Input, Exiting')

if __name__ == '__main__':  
    main()
