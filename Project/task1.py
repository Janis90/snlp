import utils
import numpy as np


def calc_levenshtein_distance(source, target):
    """Create word adjustments based on levenshtein distance.
    E.g. schielen + geschielt => __schielen + geschielt_

    Parameters
    ----------
    source : string
        Source word.
    target : string
        Target word.

    Returns
    -------
    string, string
        The modified source and target word.

    """
    if source == target:
        return source, target

    s_len = len(source) + 1
    t_len = len(target) + 1
    matrix = np.zeros((s_len, t_len))

    # calulate levenshtein distance matrix
    for i in range(s_len):
        for j in range(t_len):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
            else:
                case_1 = matrix[i - 1][j] + 1
                case_2 = matrix[i][j - 1] + 1
                equal = 0 if source[i - 1] == target[j - 1] else 1
                case_3 = matrix[i - 1][j - 1] + equal

                matrix[i][j] = min(case_1, case_2, case_3)

    # create annotated words
    source_word = ''
    target_word = ''

    i = s_len - 1
    j = t_len - 1

    # TODO: irgendwo ist noch ein fehler drin
    # (zum testen: http://www.let.rug.nl/kleiweg/lev/)
    while i != 0 or j != 0:
        if i == 0:
            source_word = '_' + source_word
            target_word = target[j - 1] + target_word
            j = j - 1
            print('i == 0: ' + str(i) + ' ' + str(j))

        elif j == 0:
            target_word = '_' + target_word
            source_word = source[i - 1] + source_word
            i = i - 1
            print('j == 0: ' + str(i) + ' ' + str(j))

        else:
            left_e = matrix[i - 1][j]
            above_e = matrix[i][j - 1]
            left_above_e = matrix[i - 1][j - 1]

            min_e = min(left_e, left_e, left_above_e)

            if min_e == above_e:
                source_word = '_' + source_word
                target_word = target[j - 1] + target_word
                j = j - 1
            elif min_e == left_e:
                target_word = '_' + target_word
                source_word = source[i - 1] + source_word
                i = i - 1
            else:
                source_word = source[i - 1] + source_word
                target_word = target[j - 1] + target_word
                i = i - 1
                j = j - 1

    print(source_word)
    print(target_word)

    return source_word, target_word


def main():
    # params = utils.read_params()

    # print(params)
     calc_levenshtein_distance('schielen', 'geschielt')

    #utils.read_file(params["train"])

    utils.generate_suffix_changing_rules("__schielen","geschielt_")
    utils.generate_prefix_changing_rules("__schielen","geschielt_")



if __name__ == "__main__":
    main()
