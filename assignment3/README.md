# assignment3 - Sentiment Analysis with Naive Bayes
- Rutger Farry & Simon Wu
- CS331
- Dr. Rebecca Hutchinson
- 8 June 2017

## Running the code
The program looks for two files, named trainingSet.txt and testSet.txt, and outputs the results to stdout. If these files don't exist, the program will crash. Specs for these files are found here: It is built in Python 3, so running them should be simple on most computers:
```bash
python3 main.py
```

## About
### Construction
The program is split into a library and executable. All the computations and processing happen in `lib.py`, while the executable, `main.py` just calls the correct functions and provides a CLI.

The code has been tested for compatibility down to Python 3.3.2. It may work with older versions, but they are not supported. :warning: The script will not work on Python 2.

### Accuracy
:chart: In our tests, the sentiment analyzer achieved **79.7% accuracy**. Some ideas for improving accuracy are: 
1. Increasing our training data
2. Spell-correcting mispelled words
3. Trimming excess characters. For example `soooooooo good` should be considered the same as `soo good`.
