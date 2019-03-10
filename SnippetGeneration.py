from Tokenizer import *
from operator import itemgetter
import os

sampleListOfSentences = ['This is a sentence', 'Luhn has a significant ranking alogrithm', 'of a and a jingle',
'Tropical Fish eat other fish, even in aquariums', 'Aquariums are where fish live']

def getDocumentTextForSnippetGeneration(fn, dir):
    """
    A helper function to get the text for a given document
    """
    basePath = os.getcwd()
    fullPath = ("%s/%s/%s") % (basePath, dir, fn, )
    f = open(fullPath,'r')
    rl = f.read()
    soup = BeautifulSoup(rl, 'html5lib')
    big_string = soup.get_text(' ')
    f.close()
    return removeBottomNumbersFromText(big_string)

def removeBottomNumbersFromText(documentText):
    """
    A helper function to remove the bottom numbers from the document text
    """
    # Sample of what we're matching as our terminating line below:
    # CA630117 ES March 17, 1982 10:10 AM
    # regex = 'CA\d\d\d\d\d\d (.+)\s(.+)\s(\d+),\s\d\d\d\d\s(.+):(.+)\s[A|P]M'
    # Due to some irregularities/typos in the cacm colleciton, we have had to make
    # our regex a little more flexible
    regex = 'CA\d\d\d\d\d\d(.*)(.+)\s(.+)\s(\d+),(.+):(.+)[A|P]M'
    pattern = re.compile(regex)
    lines = documentText.splitlines()
    outputLines = []
    for line in lines:
        m = pattern.match(line)
        if m is not None:
            return outputLines
        else:
            if line is not "":
                outputLines.append(line)
    # Should never reach this point... 
    print ("WE HAVE FAILED HORRIBLY!")
    print ("failed", documentText)



def snippetGenerator(listOfDocumentNames, tokenizedQuery, n, queryNum):
    """
    Generates a snippet for each of the documents in the corpus matching
    the document names passed into this function. The snippet is generated
    based on the query. 'n' represents the maximum amount of lines we'll include
    in the snippet. For documents which only have one line or two lines, we may be
    below n.
    """
    print ("Generating Snippets for Query Number:", queryNum)
    outputString = ""
    # tokenizedQuery = Tokenize_String(query)
    for doc in listOfDocumentNames:
        docWithExtension = doc + '.html'
        documentText = getDocumentTextForSnippetGeneration(docWithExtension, 'cacm')
        snippet = textSummarization(n, documentText, tokenizedQuery)
        outputString = outputString + "DocID: " + doc + '\n' + snippet + "\n"
    return outputString



def textSummarization(n, documentText, query):
    """
    Using a modified Luhn's Significant Factor which further stresses the importance
    of query terms being present, output at most the top 'n' amount of sentences.
    This also does Query Highlighting. 
    """
    # print ("DocumentText", documentText)
    numberOfSetencesInDocument = len(documentText)
    if numberOfSetencesInDocument < 25:
        threshold = 7 - 0.1 * (25 - numberOfSetencesInDocument)
    elif numberOfSetencesInDocument >= 25 and numberOfSetencesInDocument <= 40:
        threshold = 7
    else:
        threshold = 7 + 0.1 * (numberOfSetencesInDocument - 40)
    # print ("Sentences Amount in D:", numberOfSetencesInDocument)
    languageModelOfDocument = {}
    significantWordsSet = []
    for sentence in documentText:
        tempTokens = Tokenize_String(sentence)
        for token in tempTokens:
            if token in languageModelOfDocument.keys():
                languageModelOfDocument[token] = languageModelOfDocument[token] + 1
            else:
                languageModelOfDocument[token] = 1
    for token in languageModelOfDocument.keys():
        if languageModelOfDocument[token] > threshold:
            significantWordsSet.append(token)
        if token in query:
            significantWordsSet.append(token)
    # print ("signifance word sets", significantWordsSet)
    rankedSentences = rankSentences(documentText, significantWordsSet, query)
    rangeLimit = min(n, numberOfSetencesInDocument)
    sortedRanked = sorted(rankedSentences.items(), key = itemgetter(1), reverse = True)
    summarizedText = ""
    # print ("Sorted Rank", sortedRanked)
    i = 0
    for sentence in sortedRanked:
        if i < rangeLimit:
            newSentence = sentence[0]
            for q in query:
                # print ("Q", q)
                if q in newSentence:
                    # justQ = '\b' + q + '\b'
                    newQ = "**" + q + "**"
                    newSentence = re.sub('\\b'+q+'\\b', newQ, newSentence)
            summarizedText = summarizedText + "..." + newSentence + "...\n"

        i = i + 1
        if i > rangeLimit:
            # print ("query", query)
            # print ("snippet\n", summarizedText)
            return summarizedText
    return summarizedText
    
def rankSentences(documentText, sigWords, query):
    """
    Ranks a list of sentences by using the amount
    of appearances of significant words and query terms
    in the sentence. Currently weighted more heavily towards
    queries. 
    """
    rankedSentences = {}
    i = 0
    for sentence in documentText:
        rankedSentences[sentence] = 0
        for token in sigWords:
            if token in sentence:
                rankedSentences[sentence] = rankedSentences[sentence] + 1
        for qu in query:
            if qu in sentence:
                rankedSentences[sentence] = rankedSentences[sentence] + 3
    return rankedSentences
