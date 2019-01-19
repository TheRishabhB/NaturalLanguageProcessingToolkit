#!/usr/bin/python
import sys
import string
from nltk.util import tokenwrap
from nltk.probability import FreqDist


def word_filter(freq_dist, blacklist):
    """
    Returns a dictionary of word-frequency pairs with stop words (such as "the" or "as") filtered out.

    :param freq_dist: Frequency Distribution Object from nltk.
    :type freq_dist: FreqDist

    :param blacklist: List of words explicitly not to be shown. To be used if nltk provided list is missing some words.
        Pass empty array if not needed.
    :type blacklist: List

    :rtype dict
    """
    # Try to get list of stop words
    try:
        from nltk.corpus import stopwords
    except ImportError:
        raise ValueError(
            'Could not import one of nltk.corpus or stopwords.'
        )

    stop_words = stopwords.words('english')
    return dict((word, freq_dist[word]) for word in freq_dist if word.lower() not in stop_words and
                word not in string.punctuation and word.isalnum() and word not in blacklist)


def plot_most_common(data, num=30, title='', y_label="Frequency", line_width=2):
    # import nltk.text
    # WordFreqDist = FreqDist()
    # Try to import required libs
    try:
        from matplotlib import pylab
        from operator import itemgetter
    except ImportError:
        raise ValueError(
            'Error Importing MatPlotLib or operator.'
        )

    # Filter most frequent items, depending on value of "num" passed in. Default is 50.
    reverse_most_frequent_items = sorted(data.items(), key=itemgetter(1))[-num:]
    # The above returns highest frequency items but still lowest->highest. This flips to required order.
    # Note: This second step is required, as if reversed=True is put in the first sort, it gives values in least.
    most_frequent_items = sorted(reverse_most_frequent_items, key=itemgetter(1), reverse=True)

    # Frequencies of Items
    frequencies = [item[1] for item in most_frequent_items]
    items = [item[0] for item in most_frequent_items]

    # Customize Graph and Show
    if title:
        pylab.title(title)
    pylab.plot(frequencies, linewidth=line_width)
    pylab.ylabel(y_label)
    pylab.grid(True, color="silver")
    pylab.xticks(range(len(items)), items, rotation=90)
    pylab.show()


def find_collocations(parsed_book, blacklist, num, window_size):
    # Try to get list of stop words
    try:
        import nltk.text
        from nltk.corpus import stopwords
        from nltk.collocations import BigramCollocationFinder
    except ImportError:
        raise ValueError(
            'Could not import one of the requirements.'
        )
    ignored_words = stopwords.words('english')

    bi_gram_measures = nltk.collocations.BigramAssocMeasures()

    finder = BigramCollocationFinder.from_words(parsed_book, window_size)
    finder.apply_freq_filter(2)
    finder.apply_word_filter(lambda word: len(word) < 3 or word.lower() in ignored_words or word.lower() in blacklist)
    collocated_strings = finder.nbest(bi_gram_measures.likelihood_ratio, num)
    return [first_word + ' ' + second_word for first_word, second_word in collocated_strings]


def main():
    # Parse Book into Array
    parsed_book = open(str(sys.argv[1])).read().split()

    # Default Values and Parsing Input Values
    # Graph Values
    num_points = 30
    title = "Top " + str(num_points) + " Useful Words For " + str(sys.argv[1])

    y_label = "Frequencies"
    line_width = 3

    if "--title" in sys.argv:
        title = sys.argv[sys.argv.index("--title") + 1]

    if "--yLabel" in sys.argv:
        y_label = sys.argv[sys.argv.index("--yLabel") + 1]

    if "--lineWidth" in sys.argv:
        line_width = sys.argv[sys.argv.index("--lineWidth") + 1]

    if "--numPoints" in sys.argv:
        num_points = sys.argv[sys.argv.index("--numPoints") + 1]

    # Stop Words Values
    blacklist = []
    if "--blacklist" in sys.argv:
        blacklist = sys.argv[sys.argv.index("--blacklist") + 1].replace(" ", "").split(',')

    # Collocations Values
    num_collocations = 20
    if "--numCollocations" in sys.argv:
        num_collocations = sys.argv[sys.argv.index("--numCollocations") + 1]

    window_size = 4
    if "--windowSize" in sys.argv:
        window_size = sys.argv[sys.argv.index("--windowSize") + 1]

    # Collocations
    # Paper Explaining The Math
    # https://nlp.stanford.edu/fsnlp/promo/colloc.pdf
    print("Words Commonly Used Together:")
    print(tokenwrap(find_collocations(parsed_book, blacklist, num=int(num_collocations), window_size=int(window_size)), separator=" ; "))

    # Filter out Stop Words
    filtered_freq_dist = word_filter(FreqDist(parsed_book), blacklist)

    # Plot
    plot_most_common(filtered_freq_dist, int(num_points), title, y_label, int(line_width))


if __name__ == "__main__":
    main()
