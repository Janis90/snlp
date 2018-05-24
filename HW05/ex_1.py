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

    return uni_probs


def calc_2_gram_probabilities(bigrams, unigrams):
    bi_probs = {}

    for bi in bigrams:
        if bigrams[bi] < 2:
            continue
        bi_probs[bi] = bigrams.get(bi, 0) / float(unigrams[bi.split(" ")[0]])
    return bi_probs


def calc_3_gram_probabilities(trigrams, bigrams):
    tri_probs = {}

    for tri in trigrams:
        if trigrams[tri] < 2:
            continue
        tri_probs[tri] = trigrams.get(
            tri, 0) / float(bigrams[" ".join(tri.split(" ")[:2])])
    return tri_probs


def test_set_frequencies():
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


def calculate_perplexity(uni_probs, bi_probs, tri_probs, freq1, freq2, freq3):
    test = open("./data/train.txt", "r")
    tokens = word_tokenize(test.read())
    test.close()
    tokens = sanitize_text(tokens)

    # distribution from training data

    perplexity(0, uni_probs, tokens, freq1)
    perplexity(1, bi_probs, tokens, freq2)
    perplexity(2, tri_probs, tokens, freq3)


def perplexity(n, distribution, tokens, rel_frequencies):
    log_prob = 0
    N = len(tokens)

    for i in range(len((tokens))):
        s = " ".join(tokens[i:i + n + 1])
        log_prob += -log10(distribution[s]) * rel_frequencies.get(s, 0)
        N += 1
    perplexity = log_prob / float(N)
    print(perplexity)


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

    freq1, freq2, freq3 = test_set_frequencies()

    calculate_perplexity(unigramProbs, bigramProbs,
                         trigramProbs, freq1, freq2, freq3)

    print(bigramProbs)


if __name__ == "__main__":
    main()
