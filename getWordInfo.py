#!/usr/bin/python
import sys


def main():
    # Parse Book into Array
    word = str(sys.argv[1])

    try:
        from nltk.corpus import wordnet
        # Port Streaming
        from nltk.stem import PorterStemmer
        # Lancaster Streaming
        from nltk.stem import SnowballStemmer
        # WordNetLemmatizer
        from nltk.stem import WordNetLemmatizer
    except ImportError:
        raise ValueError(
            'Could not import nltk.corpus, ntlk.stem .'
        )

    if "--stem" in sys.argv:
        # Stem Word
        porter_stemmer = PorterStemmer()
        porter_stemmed_word = porter_stemmer.stem(word)
        if porter_stemmed_word:
            print("The Porter Stemming Algorithm changed the word to %s." % porter_stemmed_word)

        lancaster_stemmer = SnowballStemmer('english')
        lancaster_stemmed_word = lancaster_stemmer.stem(word)
        if lancaster_stemmed_word:
            print("The Lancaster Stemming Algorithm changed the word to %s." % lancaster_stemmed_word)

    if "--lemmant" in sys.argv:
        lemmatizer = WordNetLemmatizer()
        lemmantized_word = lemmatizer.lemmatize(word)
        if lemmantized_word:
            print('The Lemmatized Word is: %s' % lemmantized_word)
        print("\n")

    # Get Definition
    synsets = wordnet.synsets(word)
    definitions = [synset.definition() for synset in synsets]
    print("The definition of \"%s\" are as follows:" % word)
    if definitions:
        # Format nicely so only shows one word per line.
        print('\n'.join(definitions))
    else:
        print("No definition found.")

    # Get Synonyms
    synonyms = [synonym.name() for synset in synsets for synonym in synset.lemmas()]
    print("\nSynonyms for \"%s\" include: " % word)
    if synonyms:
        print(', '.join(synonyms).replace("_", " "))
    else:
        print("No synonyms found.")

    # Get Synonyms
    antonyms = [antonym.name() for synset in synsets for lemma in synset.lemmas() for antonym in lemma.antonyms()]
    print("\nAntonyms for \"%s\" include: " % word)
    if antonyms:
        print(', '.join(antonyms).replace("_", " "))
    else:
        print("No Antonyms Found.")


if __name__ == "__main__":
    main()
