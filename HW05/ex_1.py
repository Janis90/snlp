#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from nltk.tokenize import word_tokenize
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


def calc_n_gram_frequencies(tokens, l):
    """
    Calculate n grams frequencies based on tokens and l = ngram length
    """
    frequencies = {}

    for index, word in enumerate(tokens):
        if index > len(tokens) - l:
            break

        ngram = " ".join(tokens[index:index + l + 1])
        frequencies[ngram] = frequencies.get(ngram, 0) + 1
    return frequencies


def calc_1_gram_probabilities(unigrams, N):
    uni_probs = {}

    for u in unigrams:
        uni_probs[u] = unigrams.get(u, 0) / float(N)

    print('Unigram probabilities:' + str(uni_probs))
    return uni_probs


def calc_2_gram_probabilities(bigrams, unigrams):
    bi_probs = {}

    for bi in bigrams:
        if bigrams[bi] < 2:
            continue
        bi_probs[bi] = bigrams.get(bi, 0) / float(unigrams[bi.split(" ")[0]])
    print('Bigram probabilities:' + str(bi_probs))
    return bi_probs


def calc_3_gram_probabilities(trigrams, bigrams):
    tri_probs = {}

    for tri in trigrams:
        if trigrams[tri] < 2:
            continue
        tri_probs[tri] = trigrams.get(
            tri, 0) / float(bigrams[" ".join(tri.split(" ")[:2])])
    print('Trigram probabilities:' + str(tri_probs))
    return tri_probs


def test_set_frequencies():
    """
    Calculate rel frequencies for uni, bi and trigrams from the test data set
    """
    test = open("./data/test.txt", "r")
    tokens = word_tokenize(test.read())
    test.close()
    tokens = sanitize_text(tokens)

    freq1 = {}
    freq2 = {}
    freq3 = {}
    N = 0

    for index, word in enumerate(tokens):

        ngram = " ".join(tokens[index:index + 1])
        freq1[ngram] = freq1.get(ngram, 0) + 1

        ngram = " ".join(tokens[index:index + 1 + 1])
        freq2[ngram] = freq2.get(ngram, 0) + 1

        ngram = " ".join(tokens[index:index + 2 + 1])
        freq3[ngram] = freq3.get(ngram, 0) + 1

        N += 1

    for u in freq1:
        freq1[u] = freq1[u] / float(N)
    for bi in freq2:
        freq2[bi] = freq2[bi] / float(N - 1)

    for tri in freq3:
        freq3[tri] = freq3[tri] / float(N - 2)

    return freq1, freq2, freq3


def calculate_perplexity(uni_probs, bi_probs, tri_probs):
    """
    Calculate perplexity from the test date for uni bi and trigrams
    """
    test = open("./data/test.txt", "r")
    tokens = word_tokenize(test.read())
    test.close()
    tokens = sanitize_text(tokens)

    # distribution from training data

    perplexity(0, uni_probs, tokens)
    perplexity(1, bi_probs, tokens)
    perplexity(2, tri_probs, tokens)


def perplexity(n, distribution, tokens):
    """
    Calculate perplexity
    """
    log_prob = 0
    N = len(tokens)

    for i in range(len((tokens)) - n):
        s = " ".join(tokens[i:i + n + 1])

        try:
            log_prob += -log10(distribution[s])
        except:
            N -= 1

    perplexity = 10**(log_prob / float(N - n))

    if n == 0:
        print("Unigram Perplexity: " + str(perplexity))

    if n == 1:
        print("Bigram Perplexity: " + str(perplexity))

    if n == 2:
        print("Trigram Perplexity: " + str(perplexity))


def calculate_smoothed_perplexity(N, unigrams, bigrams, trigrams):
    alpha = 0.1

    logProb = 0
    tokens = [t for t in open("./data/test.txt")]
    N = len(tokens)

    for i in range(len(tokens) - 2):
        logProb += smoothed_perplexity(tokens[i:i + 3], N,
                                       unigrams, bigrams, trigrams, alpha)

    print("Smoothed Perplexity:",  10**(-logProb / float(N - 2)))


def smoothed_perplexity(ngram_, N, unigrams, bigrams, trigrams, alpha):
    ngram = " ".join(ngram_)
    if len(ngram_) == 1:
        return (unigrams.get(ngram, 0) + alpha) / float(N + len(unigrams) * alpha)
    elif len(ngram_) == 2:
        return (bigrams.get(ngram, 0) + alpha) / float(unigrams.get(ngram_[0], 0) + alpha * len(unigrams))
    else:
        return (trigrams.get(ngram, 0) + alpha) / float(bigrams.get(ngram_[0] + "  " + ngram_[1], 0) + alpha * len(unigrams))


def partition(lst, n):
    """
    Partition function from stack overflow
    """
    division = len(lst) / float(n)
    return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n)]


def exercise2_1():
    f = open("./data/kfold.txt", "r")

    tokens = word_tokenize(f.read())

    f.close()
    tokens = sanitize_text(tokens)
    tokens_split = partition(tokens, 5)
    cv(0.5, 0.5, tokens_split)


def cv(lamdba1, lamdba2, token_list):
    """
    Perform crossvalidation
    """

    for index, value in enumerate(token_list):
        # remove current value from list
        train_set = [x for i, x in enumerate(token_list) if i != index]
        # flatten list
        train_set = [y for x in train_set for y in x]
        test_set = value

        train_unigrams = calc_n_gram_frequencies(train_set, 0)
        train_unigram_probabilities = calc_1_gram_probabilities(
            train_unigrams, len(train_set))
        train_bigrams = calc_n_gram_frequencies(train_set, 1)
        train_bigram_probabilities = calc_2_gram_probabilities(
            train_bigrams, train_unigrams)

        interp_bigram_probs = 0
        for i in range(len(test_set) - 2):
            ngram = test_set[i:i + 2]

            """
            TODO: Fix
            interp_bigram_probs += lamdba1 * \
                train_unigram_probabilities[ngram[0]] + lamdba2 * \
                train_bigram_probabilities[" ".join(ngram)]
            """


"""
def grid_seach(tokenlist):
"""


def main():

    f = open("./data/train.txt", "r")

    tokens = word_tokenize(f.read())

    f.close()
    tokens = sanitize_text(tokens)

    unigrams = calc_n_gram_frequencies(tokens, 0)
    bigrams = calc_n_gram_frequencies(tokens, 1)
    trigrams = calc_n_gram_frequencies(tokens, 2)

    unigramProbs = calc_1_gram_probabilities(unigrams, len(tokens))
    bigramProbs = calc_2_gram_probabilities(bigrams, unigrams)
    trigramProbs = calc_3_gram_probabilities(trigrams, bigrams)

    # freq1, freq2, freq3 = test_set_frequencies()

    calculate_perplexity(unigramProbs, bigramProbs,
                         trigramProbs)

    calculate_smoothed_perplexity(len(
        tokens), unigrams, bigrams, trigrams)

    # Ex 2.1
    exercise2_1()


if __name__ == "__main__":
    main()
