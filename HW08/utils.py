import re
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from math import log10

from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer


def sanitize_text(tokens, stopwords=None):
    """
    Sanitizes a list of tokens from whitespaces and punktuations. All tokens
    will be set lowercase.

    Parameters
    ----------
        tokens : list of tokens (words)
        stopwords: string[] containing words that should be removed from the text

    Returns
    -------
        A list of tokens only consisting of alphanumeric values.
    """

    tokens = [x.lower() for x in tokens]
    regex = re.compile('[^a-z]')

    for index in range(len(tokens)):
        tokens[index] = regex.sub('', tokens[index])
        if stopwords and tokens[index] in stopwords:
            tokens[index] = ''

    # remove empty elements
    tokens = [token for token in tokens if token != '']
    return tokens


def lemma_stemming(tokens, lemma, stemmer):
    """PerfrmsLemming and Stemming.

    Parameters
    ----------
    tokens : string[]
        Description of parameter `tokens`.
    lemma : string
        Lemming type: e.g. wordnet
    stemmer : string
        Stemming type e.g. porter, snowball

    Returns
    -------
    string[]
        Lemmed / Stemmed token list

    """

    result = []
    porter_stemmer = PorterStemmer()
    wnl = WordNetLemmatizer()
    stemmer_snowball = SnowballStemmer("english")

    for token in tokens:

        out_token = ''

        if stemmer == 'porter':
            out_token = porter_stemmer.stem(token)

        if stemmer == 'snowball':
            out_token = stemmer_snowball.stem(token)

        if lemma == 'wordnet':
            out_token = wnl.lemmatize(out_token)

        result.append(out_token)

    return result


def tokenize_text_string(text_string, sanitize=True, remove_duplicates=False, stopwords=None):
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
        tokens = sanitize_text(tokens, stopwords=stopwords)

    if remove_duplicates:
        tokens = list(set(tokens))

    return tokens


def get_frequence(token_vocab, token_list):

    # compute all frequencies
    freqs = get_frequencies(token_list)
    res_freqs = {}

    for token in token_vocab:
        res_freqs[token] = freqs.get(token, 0)

    return res_freqs


def tokenize_text_file(path, sanitize=True, remove_duplicates=False, stopwords=None):
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
        tokens = tokenize_text_string(
            text_string, sanitize, remove_duplicates, stopwords=stopwords)
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
    cnt = {}

    for word in tokens:
        if word not in cnt:
            cnt[word] = 0

        cnt[word] += 1

    return cnt


def get_probabilities(vocabulary, text_tokens, get_log_prob=False):
    """
    Compute the probability of each token of the vocabulary in the given text.
    OOV words will receive probability 0. If log_prob is True and a word would get
    probability 0 this function returns -inf.

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
        if get_log_prob:
            # CAUTION - word_freq can be 0 log(0) is not definded. We return -inf for this case
            if word_freq == 0:
                probs[word] = -float('Inf')
            else:
                probs[word] = log10(word_freq) - log10(len(text_tokens))
        else:
            probs[word] = word_freq / float(len(text_tokens))

    return probs


def get_probabilities_lidstone(test_tokens, train_tokens, lidstone_lamda, vocabulary=None, get_log_prob=False):
    """
    Compute the probability of each token of the test_tokens list in the given text.
    The probability distribution will be smoothed by additive Lidstone Smoothing

    Parameters
    ----------
    test_tokens: token list containing words representing the test corpus\n
    train_tokens:  token list containing words representing the train corpus\n
    lidstone_lamda: Lidstone smoothing parameter
    vocabulary: List of tokens representing the vocabulary. If None, the vocabulary will be generated out of the train text
    get_log_prob: compute and return logarithmic probabilities with base 10

    Returns
    -------
    a dictionary with each word of the test_token list with the token and its corresponding probability as value
    """
    # create vocabulary
    if vocabulary is not None:
        vocab = list(set(vocabulary))
    else:
        vocab = list(set(train_tokens))

    # compute frequencies
    train_freqs = get_frequencies(train_tokens)

    # apply smoothing
    smoothed_probs = {}

    for test_word in set(test_tokens):

        # print("word: {} - seen {} times".format(test_word, train_freqs.get(test_word, 0)))

        if get_log_prob:
            smoothed_prob = log10(train_freqs.get(
                test_word, 0) + lidstone_lamda) - log10(len(train_tokens) + lidstone_lamda * len(vocab))
        else:
            smoothed_prob = (train_freqs.get(test_word, 0) + lidstone_lamda) / \
                float(len(train_tokens) + lidstone_lamda * len(vocab))

        smoothed_probs[test_word] = smoothed_prob

    return smoothed_probs


def get_mutual_information(c_wic, c_wioc, c_owic, c_owioc):
    """Caluclate the mututal information, based on
    formula from: https://nlp.stanford.edu/IR-book/html/htmledition/mutual-information-1.html
    Parameters
    ----------
    c_wic: integer
        Count `word_in_class`.
    c_wioc: integer
        Count`word_in_other_classes`.
    c_owic: integer
        Count`other_words_in_class`.
    c_owioc: integer
        Count `other_words_in_other_classes`.

    Returns
    -------
    type
        Description of returned object.

    """
    # total word count
    c_total = c_wic + c_wioc + c_owic + c_owioc

    mi_1 = (c_wic / float(c_total)) * log10((c_total * c_wic) /
                                            float((c_wic + c_wioc) * (c_wic + c_owic)))
    mi_2 = (c_owic / float(c_total)) * log10((c_total * c_owic) /
                                             float((c_owic + c_owioc) * (c_wic + c_owic)))
    mi_3 = (c_wioc / float(c_total)) * log10((c_total * c_wioc) /
                                             float((c_wic + c_wioc) * (c_wioc + c_owioc)))
    mi_4 = (c_owioc / float(c_total)) * log10((c_total * c_owioc) /
                                              float((c_owic + c_owioc) * (c_wioc + c_owioc)))

    return mi_1 + mi_2 + mi_3 + mi_4


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

    def lesks_similartiy(meaning_definition, context_defintions, type='default'):
        """Calculate the similarity for Lesks Algorithm .

        Parameters
        ----------
        meaning_definition : string set
            Bag of words from the dictionary for a meaning of a word
        context_definitions : string set
            Bag of words for all defintions from the context
        type: string
            Type of the similary. Can be 'default' or, 'jaccards'
        Returns
        -------
        float
            Similarity.

        """

        if type == 'default':
            return 2 * len(meaning_definition.intersection(context_defintions)) / float(len(meaning_definition) + len(context_defintions))

        if type == 'jaccards':
            return len(meaning_definition.intersection(context_defintions)) / float(len(meaning_definition.union(context_defintions)))

        print("type not mathing")

    def lesks_algorithm():
        return


if __name__ == "__main__":
    pass
