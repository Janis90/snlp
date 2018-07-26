import utils
import numpy as np
import ChangingRule


# feature_combination : [suff_rule1, suff_rule 2, ...]
suffix_changing_rules = {}

# feature_combination : ordered list [pre_rule1, pre_rule 2, ...] 
prefix_changing_rules = {}

def extract_changing_rules(inflections):
    """Generates the suffix/prefix changing rules of every inflection instance
    and stores them according to their feature

    Parameters
    ----------
    inflections : list<Inflection>
        List of inflection objects the changing rules should be extracted from
    
    """

    for inflection in inflections:

        # First the suffix changing rules          
        suffix_rules = ChangingRule.SuffixRule.generate_rules(inflection)
        for rule in suffix_rules:
            # Add to global collection of suffix rules
            if inflection.inflection_desc_list in suffix_changing_rules:
                suffix_changing_rules[inflection.inflection_desc_list].add(rule)
            else:
                suffix_changing_rules[inflection.inflection_desc_list] = set([rule])

        # Then the prefix changing rules
       
        prefix_rules = ChangingRule.PrefixRule.generate_rules(inflection)
        for rule in prefix_rules:
            # Add to global collection of prefix rules
            if str(inflection.inflection_desc_list) in prefix_changing_rules:
                prefix_changing_rules[str(inflection.inflection_desc_list)].add(rule)
            else:
                prefix_changing_rules[str(inflection.inflection_desc_list)] = set([rule])


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

    # printing the extracted rules
    print("\nPREFIX RULES:")
    for col, rules in prefix_changing_rules.items():
        print("\n{}:".format(col))
        for rule in rules:
            print("\t{}".format(rule))

    print("\nSUFFIX RULES:")
    for col, rules in suffix_changing_rules.items():
        print("\n{}:".format(col))
        for rule in rules:
            print("\t{}".format(rule))





if __name__ == "__main__":
    main()
