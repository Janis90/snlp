import utils
import numpy as np
import ChangingRule


# feature_combination : [suff_rule1, suff_rule 2, ...]
suffix_changing_rules = {}

# feature_combination : ordered list [pre_rule1, pre_rule 2, ...] 
prefix_changing_rules = {}


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

    print(source_word)
    print(target_word)

    return source_word, target_word


def extract_changing_rules(inflections):
    """
        inflections: list of inflection objects

        generates the suffix/prefix changing rules of every inflection instance
        and stores them according to their feature
    """

    for inflection in inflections:

        lemma, inflect = calc_levenshtein_distance(inflection.lemma, inflection.inflection)
        features = inflection.inflection_desc_list

        "First the suffix changing rules"        
       
        suffix_rules = ChangingRule.SuffixRule.generate_rules(lemma, inflect, features)
        for rule in suffix_rules:
            "Add to global collection of suffix rules"
            suffix_changing_rules[features] = suffix_changing_rules[features].append(rule) 


        "Then the prefix changing rules"
       
        prefix_rules = ChangingRule.PrefixRule.generate_rules(lemma, inflect, features)
        for rule in prefix_rules:
            "Add to global collection of prefix rules"
            prefix_changing_rules[features] = prefix_changing_rules[features].append(rule)


    #TODO IMPORTANT: SORT THE PREFIX CHANGING RULES 





def generate_suffix_changing_rules(a, b):

    assert len(a) == len(b)
    assert a != b

    rules = []
    rules.append("$ > $")
    suff_a = ""
    suff_b = ""
    seenStem = False

    for i in range(len(a) - 1, -1, -1):

        # entering prefix
        if seenStem and (a[i] == "_" or b[i] == "_"):
            break

        # entering stem
        if not seenStem and a[i] != "_" and b[i] != "_":
            seenStem = True

        suff_a = (a[i] + suff_a) if a[i] != "_" else suff_a
        suff_b = (b[i] + suff_b) if b[i] != "_" else suff_b

        rule = suff_a + "$ > " + suff_b + "$"
        print(rule)
        rules.append(rule)

    return rules


def generate_prefix_changing_rules(a, b):
    assert len(a) == len(b)
    assert a != b

    rules = []
    rules.append("$ > $")

    pre_a = "$"
    pre_b = "$"
    for i in range(len(a)):
        if a[i] == "_":
            pre_b += b[i]
        elif b[i] == "_":
            pre_a += a[i]
        else:
            break
    rules.append(pre_a + " > " + pre_b)

    print(rules)
    return rules


def apply_most_overlapping_suffix_rule(lemma, inflection_feature):
    
    """Given a lemma of a word and feature, apply most overlapping suffix changing rule
        e.g. lemma = "kaufen" and inflection_feature = V.PTCP;PST --> apply en$ > t$ to get "kauft" 

        output: lemma inflected by suffix changing rule 
    """

    max_rule = None
    max_score = 0

    for rule in suffix_changing_rules[inflection_feature]:
        score = rule.get_overlap_score(lemma)
        if score > max_score:
            max_rule = rule
            max_score = score

    assert max_rule
    return max_rule.apply_rule(lemma)


def apply_most_frequent_prefix_rule(lemma, inflection_feature):

    """ PRECONDITION: prefix changing rules have to be sorted by frequency.

    output: lemma inflected by most frequent prefix changing rule 
    """

    prefix_rule = prefix_changing_rules[inflection_feature][0]
    inflection = prefix_rule.apply_rule(lemma)

    return inflection




def main():
    params = utils.read_params()
    
    inflections = utils.read_file(params["train"])

    extract_changing_rules(inflections)




if __name__ == "__main__":
    main()
