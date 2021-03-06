import numpy as np

class Word():
    """The Word class represents simple words consisting of a prefix, a stem and a suffix
    """

    def __init__(self, prefix, stem, suffix):
        """Creates a Word object out of the given parameters. To split up a string into prefix, stem and suffix, use 
        a splitting algorithm like levinstein distance
        
        Parameters
        ----------
        prefix : string

        stem : string

        suffix : string        
        """
        self.prefix = prefix
        self.stem = stem
        self.suffix = suffix

    def to_string(self):
        return "{}{}{}".format(self.prefix, self.stem, self.suffix)

    def __str__(self):
        return "{}{} - {} - {}{}".format("{", self.prefix, self.stem, self.suffix, "}")


class WordSplitter():

    def __init__(self):
        pass

    def split_word(self, source, target):
        pass


class LevinsteinPartition(WordSplitter):

    def __init__(self):
        super().__init__()

    def split_word(self, source, target):
        """Splits a word into two Word objects with prefix, stem and suffix based on levenshtein distance.
        E.g. schielen + geschielt => "" + "schiele" + "n" and  "ge" + "schielt" + ""

        Parameters
        ----------
        source : string
            Source word.
        target : string
            Target word.

        Returns
        -------
        Word, Word
            The Word object instances of the source and the target word with applied prefix, stem and suffix partition

        """

        if source == target:
            return Word("", source, ""), Word("", target, "")

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

        # matrix backtracking
        while i != 0 or j != 0:
            if i == 0:
                source_word = '_' + source_word
                target_word = target[j - 1] + target_word
                j = j - 1
            elif j == 0:
                target_word = '_' + target_word
                source_word = source[i - 1] + source_word
                i = i - 1
            else:
                above_e = matrix[i - 1][j]
                left_above_e = matrix[i - 1][j - 1]

                min_e = min(above_e, above_e, left_above_e)

                if min_e == above_e:
                    target_word = '_' + target_word
                    source_word = source[i - 1] + source_word
                    i = i - 1
                elif min_e == left_above_e:
                    source_word = source[i - 1] + source_word
                    target_word = target[j - 1] + target_word
                    i = i - 1
                    j = j - 1
                else:
                    source_word = '_' + source_word
                    target_word = target[j - 1] + target_word
                    j = j - 1

        source_word_a = np.array(list(source_word))
        target_word_a = np.array(list(target_word))

        stem_mask = np.zeros(len(source_word), dtype=bool)
        prefix_mask = np.zeros(len(source_word), dtype=bool)
        suffix_mask = np.zeros(len(source_word), dtype=bool)

        for i in range(len(source_word)):
            if source_word_a[i] != "_" and target_word_a[i] != "_":
                stem_mask[i] = True

        for i in range(len(source_word)):
            if (source_word_a[i] == "_" and target_word_a[i] != "_") or (source_word_a[i] != "_" and target_word_a[i] == "_"):
                prefix_mask[i] = True
            else: 
                break

        for i in reversed(range(len(source_word))):
            if (source_word_a[i] == "_" and target_word_a[i] != "_") or (source_word_a[i] != "_" and target_word_a[i] == "_"):
                suffix_mask[i] = True
            else: 
                break

        # generate source word
        stem = "".join(source_word_a[stem_mask])
        prefix = "".join(source_word_a[prefix_mask])
        suffix = "".join(source_word_a[suffix_mask])
        prefix = prefix.replace("_", "")
        suffix = suffix.replace("_", "")

        new_source_word = Word(prefix, stem, suffix)

        # generate target word
        stem = "".join(target_word_a[stem_mask])
        prefix = "".join(target_word_a[prefix_mask])
        suffix = "".join(target_word_a[suffix_mask])
        prefix = prefix.replace("_", "")
        suffix = suffix.replace("_", "")

        new_target_word = Word(prefix, stem, suffix)

        return new_source_word, new_target_word


class KhalingXFixPartition(WordSplitter):

    def __init__(self):
        super().__init__()
        self.prefix_list = ["ʔi", "mu", "mʌ"]

        self.suffix_lists = [["ŋ", "i", "k", "n"], 
                             ["de", "tʰer", "kʰʌ"], 
                             ["ŋʌ", "nɛ", "ʌ", "u", "i", "k"], 
                             ["t", "w"], 
                             ["ʌkʌ", "iki", "ŋʌ", "ki", "ɛ", "ʌ", "u", "i"], 
                             ["si", "su", "n"], 
                             ["su", "nu", "ni"]]

    def __check_and_cut_prefix(self, input_str):

        for pos_prefix in self.prefix_list:
            if input_str.startswith(pos_prefix):

                # return prefix and the remaining word
                return pos_prefix, input_str[len(pos_prefix):]

        # if no prefix from the list found, return empty prefix
        return "", input_str

    def __check_and_cut_suffixes(self, input_string):

        res_suffixes = []

        for suffix_list in reversed(self.suffix_lists):
            for pos_suffix in suffix_list:

                # save suffix and cut off from word
                if input_string.endswith(pos_suffix):
                    res_suffixes.append(pos_suffix)

                    input_string = input_string[:len(input_string) - len(pos_suffix)]

        return input_string, reversed(res_suffixes)

    def split_word(self, source, target):
        src_prefix, scr_stem_suffix = self.__check_and_cut_prefix(source)
        src_stem, src_suffix_list = self.__check_and_cut_suffixes(scr_stem_suffix)

        source_word = Word(src_prefix, src_stem, "".join(src_suffix_list))

        tgt_prefix, tgt_stem_suffix = self.__check_and_cut_prefix(target)
        tgt_stem, tgt_suffix_list = self.__check_and_cut_suffixes(tgt_stem_suffix)

        target_word = Word(tgt_prefix, tgt_stem, "".join(tgt_suffix_list))

        # print("SOURCE: {} - TARGET: {}".format(source_word, target_word))

        return source_word, target_word



