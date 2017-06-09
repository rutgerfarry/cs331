import sys
from lib import preprocess, train_naive_bayes, test_naive_bayes

def print_test_results(results, test_docs):
    misclassified_docs = []
    for result, doc in zip(results, test_docs):
        if result != doc[1]:
            misclassified_docs.append(doc + tuple([result]))

    for doc in misclassified_docs:
        print('misclassified {}: actual: {}, expected: {}'.format(doc[0], doc[2], doc[1]))

    correct = len(test_docs) - len(misclassified_docs)
    incorrect = len(misclassified_docs)
    accuracy = correct / len(test_docs)

    print("\n")
    print("****************************************")
    print("* RESULTS:")
    print("*     Correct:   {}".format(correct))
    print("*     Incorrect: {}".format(incorrect))
    print("*")
    print("*     Accuracy:  {}".format(accuracy))
    print("****************************************")

def test(test_docs, prior, likelihood, classes, vocab):
    results = []
    for test_doc in test_docs:
        results.append(test_naive_bayes(test_doc, prior, likelihood, classes, vocab))
    print_test_results(results, test_documents)

# Prevent running if imported as a module
if __name__ == '__main__':
    classes = [0, 1]
    # perform test on the training data
    sys.stdout = open('output.txt', 'wt')
    vocab, documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')
    _, test_documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')

    prior, likelihood = train_naive_bayes(vocab, documents, classes)

    print("\n")
    print("testing on training data")
    test(documents, prior, likelihood, classes, vocab)

    # perform test on the testing data
    vocab, documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')
    _, test_documents = preprocess('testSet.txt', 'preprocessed_test.txt')

    prior, likelihood = train_naive_bayes(vocab, documents, classes)
    print("\n")
    print("testing on testing data")
    test(test_documents, prior, likelihood, classes, vocab)

