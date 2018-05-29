#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3)
    - Wortschatz (#unterschiedlicher Wörter)
    - Sprache
    - Syntax (Einfache vs. verschachtelte Sätze)
    - Wörter bestimmter Kategorien (Emotionen, Thema, ...)
    - Morphologische Eigenschaften (# Nomen, #Verben, vor allem AdjektiveØ...)
"""

import re
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from math import log10


def sanitize_text(tokens):
    """Sanizite Text:
        Lowercase
        Remove non characters
    Parameters
    ----------
    tokens : string[]
        Tokenized text

    Returns
    -------
    string[]
        Sanitized tokens.

    """

    tokens = [x.lower() for x in tokens]
    regex = re.compile('[^a-z]')

    for index in range(len(tokens)):
        tokens[index] = regex.sub('', tokens[index])

    # remove empty elements
    tokens = [token for token in tokens if token != '']
    return tokens


def getWordFrequencies(tokens):
    cnt = Counter()

    for word in tokens:
        cnt[word] += 1

    return cnt


def getTokens(path):
    f = open(path, "r")

    tokens = word_tokenize(f.read())

    tokens = sanitize_text(tokens)

    f.close()

    return tokens


def plot_most_common_words(cnt, word_count, title):
    labels = [None] * len(cnt.most_common(word_count))
    frequencies = [None] * len(cnt.most_common(word_count))

    for idx, value in enumerate(cnt.most_common(word_count)):
        labels[idx] = value[0]
        frequencies[idx] = value[1]

    y_pos = np.arange(len(labels))

    plt.bar(y_pos, frequencies, align='center', alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.xlabel('Most common words')
    plt.ylabel('Word Frequencies')
    plt.title(title)

    plt.show()


def ex_4():
    cnt = getWordFrequencies(sanitize_text(
        getTokens('./corpus/james/Henry James___1.txt')))
    plot_most_common_words(cnt, 10, 'Henry James 1')

    cnt = getWordFrequencies(sanitize_text(
        getTokens('./corpus/james/Henry James___2.txt')))
    plot_most_common_words(cnt, 10, 'Henry James 2')

    cnt = getWordFrequencies(sanitize_text(
        getTokens('./corpus/james/Henry James___3.txt')))
    plot_most_common_words(cnt, 10, 'Henry James 3')

    cnt = getWordFrequencies(sanitize_text(
        getTokens('./corpus/london/Jack London___1.txt')))
    plot_most_common_words(cnt, 10, 'Jack London 1')

    cnt = getWordFrequencies(sanitize_text(
        getTokens('./corpus/london/Jack London___2.txt')))
    plot_most_common_words(cnt, 10, 'Jack London 2')

    cnt = getWordFrequencies(sanitize_text(
        getTokens('./corpus/london/Jack London___3.txt')))
    plot_most_common_words(cnt, 10, 'Jack London 3')


def smooth_lidstone(token_count, total_tokens, alpha, len_vocabulary):
    return (token_count + alpha) / float(total_tokens + alpha * len_vocabulary)


def calc_word_frequencies(tokens):
    """Calculate absolute word frequencies.

        Parameters
        ----------
        tokens:  string[]
                 Tokens of a language corpus.
    """
    if (len(tokens) == 0):
        print('no words received')
        return

    word_frequencies = {}

    # count word frequencies
    for word in tokens:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    return word_frequencies


def calc_bayes(tokens, frequencies, n, v, class_prob, alpha):
    """Calculate the bayes probability for a given class.

    Parameters
    ----------
    tokens : string[]
        Tokens from the test set.
    frequencies : dict
        Relative word frequencies for a given class.
    n : integer
        Number of tokens for a given class
    v : integer
        Vocabulary size for a given class.
    class_prob : float
        Class probability for a given class
    alpha : float
        Alpha value for the lidstone smoothing

    Returns
    -------
    foat
        Bayes probability for a given class.

    """

    probability = log10(class_prob)
    # denominator = 0

    for word in tokens:
        probability += log10(smooth_lidstone(frequencies.get(word, 0), n, alpha, v))
        # TODO: denominator = log()

    return probability


def calc_bayes_classification(tokens, freq_lists, n_lists, v_lists, class_prob_lists, alpha):
    """Calculate classification for n classes.

    Parameters
    ----------
    tokens : string[]
        Tokens from the test set.
    freq_lists: dict[]
        List containing the relative word frequencies for each class
    n_lists : integer[]
        Total number for tokens for each class
    v_lists : integer[]
        Vocabulary size for each class.
    class_prob_lists : float
        Description of parameter `class_prob_lists`.
    alpha : float
        Alpha value for the lidstone smoothing

    Returns
    -------
    max_index: integer
        Index of the element with the highest bayes probability
    bayes_classification: float[]
        Array containing bayes probabilities for each class


    """
    bayes_classification = []

    for index in range(len(freq_lists)):
        bayes_classification.append(calc_bayes(
            tokens, freq_lists[index], n_lists[index], v_lists[index], class_prob_lists[index], alpha))

    max_value = max(bayes_classification)
    max_index = bayes_classification.index(max_value)

    return max_index, bayes_classification


def ex_5():
    ALPHA = 0.00001

    tokens_james_1 = sanitize_text(
        getTokens('./corpus/james/Henry James___1.txt'))
    tokens_james_2 = sanitize_text(
        getTokens('./corpus/james/Henry James___3.txt'))
    tokens_james_3 = sanitize_text(
        getTokens('./corpus/james/Henry James___3.txt'))
    tokens_james = tokens_james_1 + tokens_james_2 + tokens_james_3

    tokens_london_1 = sanitize_text(
        getTokens('./corpus/london/Jack London___1.txt'))
    tokens_london_2 = sanitize_text(
        getTokens('./corpus/london/Jack London___2.txt'))
    tokens_london_3 = sanitize_text(
        getTokens('./corpus/london/Jack London___3.txt'))

    tokens_london = tokens_london_1 + tokens_london_2 + tokens_london_3

    word_frequencies_james = calc_word_frequencies(tokens_james)
    v_james = len(word_frequencies_james)
    n_james = len(tokens_james)

    word_frequencies_london = calc_word_frequencies(tokens_london)
    v_london = len(word_frequencies_london)
    n_london = len(tokens_london)

    tokens_test_1 = sanitize_text(getTokens('./corpus/test/test1.txt'))
    tokens_test_2 = sanitize_text(getTokens('./corpus/test/test2.txt'))
    tokens_test_3 = sanitize_text(getTokens('./corpus/test/test3.txt'))

    for tokens in [tokens_test_1, tokens_test_2, tokens_test_3]:

        index, probs = calc_bayes_classification(tokens, [word_frequencies_james, word_frequencies_london], [
                                                 n_james, n_london], [v_james, v_london], [0.5, 0.5], ALPHA)
        if index == 0:
            print("Classified as JAMES with " +
                  str(probs[0]) + " vs. " + str(probs[1]) + " log probs")
        else:
            print("Classified as LONDON with " +
                  str(probs[1]) + " vs. " + str(probs[0]) + " log probs")


def main():
    ex_4()
    ex_5()


if __name__ == "__main__":
    main()
