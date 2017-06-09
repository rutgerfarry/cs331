import re
from math import log
from collections import defaultdict

non_alphanum = re.compile(r'[\W_]+')
flatten = lambda l: [item for sublist in l for item in sublist]

def process_word(word):
    return non_alphanum.sub('', word.lower())

def process_document(document):
# Returns a tuple. The first element is the review split into array of words.
# The second element is an int indicating whether the review was positive.
    return (
        [process_word(word) for word in document.split()][:-1],
        int(document.split()[-1])
    )

def format_document(document, vocab):
    return (
        ','.join(['1' if word in document[0] else '0' for word in vocab])
        + ',' + str(document[1])
    )

def preprocess(infilename, outfilename):
# Returns a tuple in the form of (vocab, documents).
# Vocab: a set of words, e.g. { 'great', 'steak', 'gross', ... }
# Documents: a tuple containing the array of words in the document followed
# by the sentiment of the document, represented by a 1 or 0, e.g.
# (['i', 'liked', 'the', 'food'], 1)

    # Process input file
    infile = open(infilename, 'r')
    outfile = open(outfilename, 'w')
    raw_documents = infile.read().splitlines()
    documents = [process_document(document) for document in raw_documents]
    vocab = {process_word(word) for document in raw_documents for word in document.split()[:-1]}
    vocab.discard('')
    infile.close()

    # Format text for outfile and write
    formatted_vocab = ','.join(sorted(list(vocab)))
    formatted_documents = '\n'.join([format_document(document, vocab) for document in documents])
    outfile.write(formatted_vocab + '\n' + formatted_documents)
    outfile.close()

    return vocab, documents

def train_naive_bayes(vocab, documents, classes):
    logprior = {}
    loglikelihood = defaultdict(dict)
    big_doc = {}

    def get_logprior(documents, c):
        class_document_count = len([doc for doc in documents if doc[1] == c])
        total_document_count = len(documents)
        return log(class_document_count / total_document_count)

    def get_bigdoc(documents, c):
        return flatten([doc[0] for doc in documents if doc[1] == c])

    for c in classes:
        logprior[c] = get_logprior(documents, c)
        big_doc[c] = get_bigdoc(documents, c)
        words_in_class_count = sum([big_doc[c].count(w) for w in vocab])

        for word in vocab:
            word_count = big_doc[c].count(word)
            loglikelihood[word][c] = log((word_count + 1) /
                                         (words_in_class_count + 1))

    return logprior, loglikelihood

# Prevent running if imported as a module
if __name__ == '__main__':
    data = preprocess('trainingSet.txt', 'preprocessed_train.txt')
    (logP, logL) = train_naive_bayes(data[0], data[1], [0, 1])
    print('prior:::')
    print(logP)
    print('likelihood:::')
    print(logL)
