#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3)
    - Wortschatz (#unterschiedlicher Wörter)
    - Syntax (Einfache vs. verschachtelte Sätze)
    - Wörter bestimmter Kategorien (Emotionen,...)
    - Morphologische Eigenschaften (# Nomen, #Verben, vor allem AdjektiveØ...)
"""

import re
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


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


def main():
    ex_4()


if __name__ == "__main__":
    main()
