import utils
import numpy as np
from ChangingRule import SuffixRule, PrefixRule, RuleCollection
from UniMorph import UniMorph, FeatureCollection

def prepare_test_data(inflections):

    test_lemmas = []
    test_feature_descs = []
    test_ground_truth = []

    for inflection in inflections:
        test_lemmas.append(inflection.lemma.to_string())
        test_feature_descs.append(inflection.inflection_desc_list)
        test_ground_truth.append(inflection.inflection.to_string())

    return test_lemmas, test_feature_descs, test_ground_truth

def inflect_data(lemma_list, feature_desc_list, prefix_rule_col, suffix_rule_col):

    inflected_data = []

    for i in range(len(lemma_list)):
        cur_lemma = lemma_list[i]
        cur_features = feature_desc_list[i]

        # get best rules
        best_prefix_rule = prefix_rule_col.get_highest_count_rule(cur_lemma, cur_features)
        best_suffix_rule = suffix_rule_col.get_highest_overlap_rule(cur_lemma, cur_features)

        # use empty rule if no rule matches
        if best_suffix_rule is None:
            best_suffix_rule = SuffixRule.empty_rule(cur_features)

        # use empty rule if no rule matches
        if best_prefix_rule is None:
            best_prefix_rule = PrefixRule.empty_rule(cur_features)

        # apply rules on lemma
        inflected_lemma = best_suffix_rule.apply_rule(cur_lemma)
        inflected_lemma = best_prefix_rule.apply_rule(inflected_lemma)

        inflected_data.append(inflected_lemma)

    return inflected_data


def compute_accuracy(predictions, ground_truth, verbose=False):

    total_count = len(predictions)
    correct = 0

    if verbose:
        print("prediction\t-\tground truth\t\tCorrect?")
        print("--------------------------")

    for i in range(total_count):

        if predictions[i] == ground_truth[i]:
            correct += 1

        if verbose:
            print("{}\t-\t {}\t\t{}".format(predictions[i], ground_truth[i], predictions[i] == ground_truth[i]))
            
    return correct/total_count



def main():
    params = utils.read_params()
    
    # TODO: Respect parameters!

    # Create rules from training
    train_inflections = utils.read_file(params["train"])
    prefix_rule_collection, suffix_rule_collection = RuleCollection.create_rule_collections(train_inflections)

    test_inflections = utils.read_file(params["test"])
    test_lemmas, test_feature_descs, test_ground_truth = prepare_test_data(test_inflections)

    predictions = inflect_data(test_lemmas, test_feature_descs, prefix_rule_collection, suffix_rule_collection)

    acc = compute_accuracy(predictions, test_ground_truth, verbose=True)

    print("Training Samples: {}".format(len(train_inflections)))
    print("Test Samples: {}".format(len(test_inflections)))
    print("Accuracy: {}%".format(acc * 100))
    

    # # Create testing data

    # lemma = "verkaufen"
    # features_string = "V.PTCP;PST"

    # feature_col = FeatureCollection.create_feature_collection(features_string)

    # best_suffix_rule = suffix_rule_collection.get_highest_overlap_rule(lemma, feature_col)

    # # use empty rule if no rule matches
    # if best_suffix_rule is None:
    #     best_suffix_rule = SuffixRule.empty_rule(feature_col)

    # best_prefix_rule = prefix_rule_collection.get_highest_count_rule(lemma, feature_col)

    # # use empty rule if no rule matches
    # if best_prefix_rule is None:
    #     best_prefix_rule = PrefixRule.empty_rule(feature_col)

    # inflected_lemma = best_suffix_rule.apply_rule(lemma)
    # inflected_lemma = best_prefix_rule.apply_rule(inflected_lemma)

    # print(best_suffix_rule)
    # print(prefix_rule_collection)
    # print(inflected_lemma)

    

    # perfix1, stem1, suffix1 = apply_most_overlapping_suffix_rule(lemma, feature_col)
    # perfix2, stem2, suffix2 = apply_most_overlapping_prefix_rule(lemma, feature_col)
    # final = prefix2, stem1, suffix1


if __name__ == "__main__":
    main()
