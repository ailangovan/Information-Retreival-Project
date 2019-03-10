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

# encodes raw positions
def delta_encode(position_list):
    last_pos = position_list[0]
    output = [last_pos]
    for i in range(1, len(position_list)):
        output.append(position_list[i] - last_pos)
        last_pos = position_list[i]
    return output

# decodes a delta encoded postion list
def delta_decode(delta_list):
    output = [delta_list[0]]
    for i in range(1, len(delta_list)):
        output.append(output[i - 1] + delta_list[i])
    return output

# output function
def write_index_to_file(index, ngram, type):
    f = open(ngram + '_' + type + '.txt', 'w+')
    for term in index:
        f.write(term + ',\t' + str(index[term].list_length) + ',\t')
        for entry in index[term].inverted_list:
            f.write(entry[0] + ':' + str(entry[1]) + '\t')
        f.write('\n')
    f.close()

def Indexer(token_dict):

    # master indexes and document_term_count data structures
    unigram_index_tf = {}
    unigram_index_pos = {}
    doc_term_counts = {}

    # create a partial index for each document in the corpus, then merge into the main index
    for file in token_dict:
        tokens = token_dict[file]
        unigram_freqs = {}
        number_unigrams = 0
        unigram_positions = {}

        for i in range(0, len(tokens)):
            if not unigram_freqs.get(tokens[i]):
                unigram_freqs[tokens[i]] = 1
                unigram_positions[tokens[i]] = [i]

            else:
                unigram_freqs[tokens[i]] += 1
                unigram_positions[tokens[i]].append(i)
            number_unigrams += 1

        for term in unigram_positions:
            unigram_positions[term] = delta_encode(unigram_positions[term])

        doc_term_counts[file] = number_unigrams

        merge_partial_index(unigram_index_tf, unigram_freqs, file)
        merge_partial_index(unigram_index_pos, unigram_positions, file)

    write_index_to_file(unigram_index_tf, 'unigram', 'frequency')
    write_index_to_file(unigram_index_pos, 'unigram', 'positional')

    f = open('Doc_Term_Counts.txt', 'w+')
    for did in doc_term_counts:
        terms = doc_term_counts[did]
        f.write(did + ' unigrams: ' + str(terms) + '\n')
    f.close()
