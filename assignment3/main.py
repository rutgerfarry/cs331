from lib import preprocess, train_naive_bayes, test_naive_bayes

def print_test_results(results, test_docs):
    misclassified_docs = []
    for result, doc in zip(results, test_docs):
        if result != doc[1]:
            misclassified_docs.append(doc + tuple([result]))

    for doc in misclassified_docs:
        print(f'misclassified {doc[0]}: actual: {doc[2]}, expected: {doc[1]}')

    correct = len(test_docs) - len(misclassified_docs)
    incorrect = len(misclassified_docs)
    accuracy = correct / len(test_docs)

    print("\n")
    print("****************************************")
    print("* RESULTS:")
    print(f"*     Correct:   {correct}")
    print(f"*     Incorrect: {incorrect}")
    print("*")
    print(f"*     Accuracy:  {accuracy}")
    print("****************************************")

def test(test_docs, prior, likelihood, classes, vocab):
    results = []
    for test_doc in test_docs:
        results.append(test_naive_bayes(test_doc, prior, likelihood, classes, vocab))
    print_test_results(results, test_documents)

# Prevent running if imported as a module
if __name__ == '__main__':
    classes = [0, 1]
    vocab, documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')
    _, test_documents = preprocess('testSet.txt', 'preprocessed_test.txt')

    prior, likelihood = train_naive_bayes(vocab, documents, classes)

    test(test_documents, prior, likelihood, classes, vocab)
