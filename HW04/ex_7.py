import nltk
import re
import matplotlib.pyplot as plt
import numpy as np
# nltk.download('gutenberg')


def sanitize_text(tokens):
    tokens = [x.lower() for x in tokens]
    regex = re.compile('[^a-z]')

    variations_you = ['your', 'yours']
    remove = ['ll', 've', 're']

    for index in range(len(tokens)):
        if tokens[index] in variations_you:
            tokens[index] = 'you'

        if tokens[index] in remove:
            tokens[index] = ''

        tokens[index] = regex.sub('', tokens[index])

    tokens = [token for token in tokens if token != '']
    return tokens


def write_file(file_path, tokens):
    f = open(file_path, 'w')
    f.write(' '.join(tokens))
    f.close()


def calc_correlation(distance, tokens):
    YOU = 'you'
    # Count you with distance d
    count_you_sequence = 0

    # count how often the word you appears in the text
    count_you = tokens.count(YOU)

    for i in range(len(tokens) - distance):
        if tokens[i] == YOU and tokens[i + distance] == YOU:
            count_you_sequence += 1

    if count_you_sequence == 0:
        print('No instance of you with distance d = ' + str(distance))
        return 0

    rel_freq_you_sequence = count_you_sequence / float(len(tokens) - distance)
    rel_freq_total = count_you / float(len(tokens))

    corr = rel_freq_you_sequence / float(rel_freq_total * rel_freq_total)
    #print("Correlation distance " + str(distance) + " :" + str(corr))
    print(corr)
    return corr


def plot_correlation(tokens, max_distance):
    distances = np.zeros(max_distance)
    correlations = np.zeros(max_distance)

    for d in range(0, max_distance):
        distances[d] = d + 1
        correlations[d] = calc_correlation(d + 1, tokens)

    plt.scatter(distances, correlations)
    plt.show()


def main():
    text = nltk.corpus.gutenberg.words('carroll-alice.txt')
    tokens = sanitize_text(text)
    write_file('test2.txt', tokens)

    plot_correlation(tokens, 50)


if __name__ == "__main__":
    main()
