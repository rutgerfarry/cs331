import re

non_alphanum = re.compile(r'[\W_]+')

def process_word(word):
    return non_alphanum.sub('', word.lower())

def process_line(line):
# Returns a tuple. The first element is the review split into array of words.
# The second element is an int indicating whether the review was positive.
    return ([process_word(word) for word in line.split()][:-1], line.split()[-1])

def format_line(line, vocab):
    return ",".join(['1' if word in line[0] else '0' for word in vocab]) + "," + str(line[1])

def preprocess(infilename, outfilename):
    # Process input file
    infile = open(infilename, 'r')
    outfile = open(outfilename, 'w')
    raw_lines = infile.read().splitlines()
    lines = [process_line(line) for line in raw_lines]
    vocab = {process_word(word) for line in raw_lines for word in line.split()[:-1]}
    vocab.discard('')
    infile.close()

    # Process text for outfile and write
    formatted_vocab = ",".join(sorted(list(vocab)))
    formatted_lines = "\n".join([format_line(line, vocab) for line in lines])
    outfile.write(formatted_vocab + '\n' + formatted_lines)

    return vocab, lines

preprocess("trainingSet.txt", "preprocessed_train.txt")
