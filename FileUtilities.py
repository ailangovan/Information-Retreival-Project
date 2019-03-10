import re
import warnings
import os
from operator import itemgetter

def docSizes(filePath):
    """
    Extracts the document sizes into a dict struct
    {docID: DocSize}
    """
    regex = "(.+)\sunigrams:\s(\d+)"
    patten = re.compile(regex)
    docs = {}
    unmatched = 0
    matchedSuccesfully = 0
    with open(filePath) as textualInvertedIndex:
        lines = textualInvertedIndex.readlines()
        lineNumber = 0
        for line in lines:
            lineNumber += 1
            m = patten.match(line)
            if m is not None:
                docs[m.group(1)] = m.group(2)
                matchedSuccesfully += 1
            else:
                unmatched += 1 
        if unmatched > 0 or matchedSuccesfully != lineNumber:
            warnings.warn("Error with Doc Index Regex")
            return
        # print (invertedIndex)
    return docs


def recreateIndexFromTextFile(filePath):
    """
    Recreates the Inverted Index from a given text file. 
    Allows the user to bypass having to index every time they wish
    to utilize the program.
    """
    regex = "(.+),\s(\d+),\s(.+)"
    patten = re.compile(regex)
    docNumRegex = "(.+):(\d+)"
    pDNR = re.compile(docNumRegex)
    invertedIndex = {}
    docLength = {}
    with open(filePath) as textualInvertedIndex:
        lines = textualInvertedIndex.readlines()
        lineNumber = 0
        matchedSuccesfully = 0
        unmatched = 0
        for line in lines:
            lineNumber += 1
            m = patten.match(line)
            if m is not None:
                docs = []
                tempList = m.group(3).split()
                tupleList = {}
                for tup in tempList:
                    mDNR = pDNR.match(tup)
                    if mDNR is None:
                        warnings.warn("We did not match the tuple")
                    # actualTuple = (mDNR.group(1), mDNR.group(2))
                    tupleList[mDNR.group(1)] = mDNR.group(2)
                invertedIndex[m.group(1)] = tupleList
                docLength[m.group(1)] = m.group(2)
                matchedSuccesfully += 1
            else:
                unmatched += 1 
        if unmatched > 0 or matchedSuccesfully != lineNumber:
            warnings.warn("Error with Inverted Index Regex")
        # print (invertedIndex)
    return invertedIndex, docLength
    # return invertedIndex, d


def outputTop(numberToOutput, query, results, scoringMethod, query_number, stopping):
    """ 
    Outputs the top (e.g. 100) ranked scores to a fileName for a list of queries
    """
    basePath = os.getcwd()
    # filename = [scoring method_query_number.txt]
    filename = scoringMethod+'_'+str(query_number)
    if stopping:
        filename += '_stopping'
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

def outputTop_qe(numberToOutput, query, results, scoringMethod, query_number, stopping):
    """ Outputs the top (e.g. 100) ranked scores to a fileName for a list of queries"""
    basePath = os.getcwd()
    # filename = [scoring method_query_number.txt]
    filename = 'bm25' + '_' + str(query_number) + '_query_enrichment.txt'
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
    output.close()

def outputSnippet(query, snippetString, function_type, query_number, stopping):
    """
    Outputs the given generated snippets for viewing in a file.
    """
    basePath = os.getcwd()
    filename = function_type+'_'+"Query"+str(query_number)
    if stopping:
        filename += "stoppingIncluded"
    else:
        filename += "noStopping"
    filename += '.txt'
    filePath = "%s/Snippets/%s" % (basePath, filename)
    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print("File path incorrect or does not exist")
    output = open(filePath, 'w')
    lineOne = "Query: %s" % (query, )
    output.write(lineOne + "\n")
    output.write(snippetString)
    output.close()
