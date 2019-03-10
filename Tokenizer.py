import os, sys, re
from bs4 import BeautifulSoup

def get_tokens_from_file(fn, dir):
    f = open('./' + dir + '/' + fn,'r')
    rl = f.read()
    soup = BeautifulSoup(rl, 'html5lib')
    big_string = soup.get_text(' ')
    tokens = big_string.split(' ')
    output = []
    for token in tokens:
        if '\t' not in token:
            if '\n' in token:
                token = token.split('\n')
                for t in token:
                    if t != '':
                        output.append(t)
                continue
            elif token != '':
                output.append(token)

    f.close()

    return output

# As named, sets everything to lower case
def case_fold(tokens):
    output = []
    for token in tokens:
        output.append(token.lower())
    return output

# Manages the removal of appropriate punctuation
def clear_punctuation(tokens):
    output = []
    for token in tokens:
        token_is_num = False
        for char in token:
            if char.isdigit():
                token_is_num = True
        if token_is_num:
            temp = process_number(token)
        else:
            temp = process_non_number(token)
        if temp:
            output.append(temp)
    return output

# removes all punctuation but - that are between two letters
# help from https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
def process_non_number(token):
    temp = ''.join(e for e in token if e.isalnum() or e == '-')
    if len(temp) == 0:
        return None
    if temp[0] == '-':
        temp = temp[1:]
        if len(temp) == 0:
            return None
    if temp[len(temp) -1] == '-':
        temp = temp[:len(temp) - 1]
    return temp

# Removes all punctuation besides ',' and '.' for numbers
def process_number(token):
    if len(token) == 0:
        return None

    while len(token) != 1 and not token[len(token) - 1].isalnum():
        token = token[:len(token) - 1]

    if len(token) == 1 and not token.isalnum():
        return None

    if token[0] != '-' and not token[0].isdigit():
        while len(token) != 1 and not token[0].isalnum():
            token = token[1:]
        if len(token) == 1 and not token.isalnum():
            return None

    return re.sub('[^0-9a-zA-Z\-:,.]','', token)

def Tokenizer(directory):

    tokens = {}

    for filename in os.listdir(directory):
        if '.html' not in filename:
            continue

        file_tokens = get_tokens_from_file(filename, directory)

        if '-nf' not in sys.argv:
            file_tokens = case_fold(file_tokens)
        if '-np' not in sys.argv:
            file_tokens = clear_punctuation(file_tokens)

        tokens[filename[:len(filename) - 5]] = file_tokens

    return tokens

def Tokenize_String(string):
    split = string.split()
    tokens = case_fold(split)
    tokens = clear_punctuation(tokens)
    return tokens
