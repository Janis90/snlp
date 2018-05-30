import re
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from math import log10


def sanitize_text(tokens):
    """
    Sanitizes a list of tokens from whitespaces and punktuations. All tokens 
    will be set lowercase.

    Parameters
    ----------
        tokens : list of tokens (words)

    Returns
    -------
        A list of tokens only consisting of alphanumeric values.
    """

    tokens = [x.lower() for x in tokens]
    regex = re.compile('[^a-z]')

    for index in range(len(tokens)):
        tokens[index] = regex.sub('', tokens[index])

    # remove empty elements
    tokens = [token for token in tokens if token != '']
    return tokens


def tokenize_text_string(text_string, sanitize=True, remove_duplicates=False):
    """
    Reads a text string and creates a list of single words.

    Parameters
    ----------
        text_string: text string to be tokenized
        sanitize: Removes whitespaces and punctuations if True
        remove_duplicates: Each token will only appear once

    Returns
    ------
        A list of tokens
    """
    tokens = word_tokenize(text_string)

    if sanitize:
        tokens = sanitize_text(tokens)

    if remove_duplicates:
        tokens = list(set(tokens))

    return tokens


def tokenize_text_file(path, sanitize=True, remove_duplicates=False):
    """
    Reads a text file and creates a list of single words.

    Parameters
    ----------
        path: filepath of the text file
        sanitize: Removes whitespaces and punctuations if True
        remove_duplicates: Each token will only appear once

    Returns
    ------
        A list of tokens
    """
    with open(path, 'r') as f:
        text_string = f.read()
        tokens = tokenize_text_string(text_string, sanitize, remove_duplicates)
    return tokens


def get_frequencies(tokens):
    """
    Counts the occurrences of tokens in a token list
    Parameters
    ---------
        tokens: list of tokens
    Returns
    -------
        A dictionary with the tokens as keys and the count as values.
    """
    cnt = Counter()

    for word in tokens:
        cnt[word] += 1

    return cnt


def get_probabilities(vocabulary, text_tokens):
    """
    Compute the probability of each token of the vocabulary in the given text.
    OOV words will receive probability 0.

    Parameters
    ----------
    vocabulary: token list containing words representing the vocabulary
    text_tokens: token list of words in a text

    Returns
    -------
    a dictionary with each word of the vocabulary as token an its corresponding probability as value
    """
    # make sure vocabulary is a set
    vocabulary = list(set(vocabulary))

    # size of text must not be 0
    assert len(vocabulary) > 0

    # get frequencies of words in text
    freqs = get_frequencies(text_tokens)

    # compute the probabilites of the words in the vocabulary
    probs = {}

    for word in vocabulary:
        word_freq = freqs.get(word, 0)
        probs[word] = word_freq / float(len(text_tokens))

    return probs


def get_probabilities_lidstone(vocabulary, text_tokens, lidstone_lamda, get_log_prob):
    """
    Compute the probability of each token of the vocabulary in the given text.
    The probability distribution will be smoothed by additive Lidstone Smoothing

    Parameters
    ----------
    vocabulary: token list containing words representing the vocabulary\n
    text_tokens: token list of words in a text\n
    lidstone_lamda: Lidstone smoothing parameter

    Returns
    -------
    a dictionary with each word of the vocabulary as token and its corresponding probability as value
    """
    # make sure vocabulary is a set
    vocabulary = list(set(vocabulary))

    # size of text must not be 0
    assert len(vocabulary) > 0

    # get frequencies of words in text
    freqs = get_frequencies(text_tokens)

    # compute the probabilites of the words in the vocabulary
    probs = {}

    for word in vocabulary:
        word_freq = freqs.get(word, 0)

        if get_log_prob:
            probs[word] = log10(word_freq + lidstone_lamda) - log10(len(text_tokens) + lidstone_lamda * len(vocabulary))
        else:
            probs[word] = (word_freq + lidstone_lamda) / float(len(text_tokens) + lidstone_lamda * len(vocabulary))

    return probs


def compute_joint_probability(token_list, token_probabilities, use_log_prob=False):
    """
    Computes the joint probability of the occurrence of a sequence of words given the probabilities of the single words.

    Parameters
    ---------
    token_list: token list containing the words for which the probability should be computed
    token_probabilities: dictionary of probabilities which contains probabilites of the single words in token_list
    to_log_prob: If True, returns the logarithmic probability to the base 10

    Returns
    -------
    joint porbability value of the occurence of the words in token_list 
    --> P(w1) * P(w2) * ... * P(wn)
    """

    log_prob = 0

    for word in token_list:

        # do not allow zero probabilites
        assert word in token_probabilities

    if use_log_prob:
        log_prob += token_probabilities[word]
    else:
        log_prob += log10(token_probabilities[word])

    if use_log_prob:
        return log_prob

    return 10**log_prob

if __name__ == "__main__":

    sample_text = "hallo hallo Sven lol nein"

    vocab = tokenize_text_string(sample_text, True, True)
    text = tokenize_text_string(sample_text, True, False)

    probs = get_probabilities(vocab, text)

    print(probs)
    print("\n")
    print(compute_joint_probability(text, probs))

