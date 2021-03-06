import implementation.utils as utils
import numpy as np
from implementation.ChangingRule import SuffixRule, PrefixRule, ConditionalRule, RuleCollection
from implementation.UniMorph import UniMorph, FeatureCollection
from implementation.Inflection import SplitMethod

def prepare_test_data(inflections):
    """Creates out of a list of inlections three lists containing all lemmas, all feature lists and the expected inflection
    
    Parameters
    ----------
    inflections : List<Inflection>
        List of inflection instances extracted from a dataset for which the data should be extracted
    
    Returns
    -------
    List<string>, List<FeatureCollection>, List<string>
        3 lists containing all relevant information from the data
    """

    test_lemmas = []
    test_feature_descs = []
    test_ground_truth = []

    for inflection in inflections:
        test_lemmas.append(inflection.lemma.to_string())
        test_ground_truth.append(inflection.inflection.to_string())
        test_feature_descs.append(inflection.inflection_desc_list)

    return test_lemmas, test_feature_descs, test_ground_truth


def inflect_data(lemma_list, feature_desc_list, prefix_rule_col, suffix_rule_col):
    """Applies learned rules in rule collections to a list of lemmas with corresponding FeatureCollections
    
    Parameters
    ----------
    lemma_list : List<string>
        List of lemma strings that should be inflected
    feature_desc_list : List<FeatureCollection>
        List of FeatureCollection instances describing how the corresponding lemma should be inflected
    prefix_rule_col : RuleCollection
        RuleCollection instance containing all prefix rules that can be applied
    suffix_rule_col : RuleCollection
        RuleCollection instance containin all suffix rules that can be applied
    
    Returns
    -------
    List<string>
        List of inflected lemma strings
    """

    inflected_data = []
    assert(len(lemma_list) == len(feature_desc_list))

    for i in range(len(lemma_list)):
        cur_lemma = lemma_list[i]
        cur_features = feature_desc_list[i]

        # get best rules
        best_prefix_rule = prefix_rule_col.get_highest_count_rule(cur_lemma, cur_features)
        # print(best_prefix_rule)
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
    """Compares the ith prediction with the ith ground truth values and computes the overall accuracy.
    
    Parameters
    ----------
    predictions : List<string>
        List containing all predicted inflections
    ground_truth : List<string>
        List containing all real (estimated) inflections
    verbose : bool, optional
        If True, prints for each prediction, the ground truth (the default is False, which)
    
    Returns
    -------
    Float
        Final accuracy value indicating how many samples are corectly predicted
    """


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
            
    return correct, correct/float(total_count)

def main():
    
    # read and parse the cli parameters
    params = utils.read_params()
    
    # create rules from training with levinstein splitting
    train_inflections = utils.read_file(params["train"], split_method=SplitMethod.LEVINSTEIN)

    # create rule collection out of the inflections
    prefix_rule_collection, suffix_rule_collection = RuleCollection.create_rule_collections(train_inflections)

    # create test set
    test_inflections = utils.read_file(params["test"], split_method=SplitMethod.LEVINSTEIN)

    # prepare datasets for testing
    test_lemmas, test_feature_descs, test_ground_truth = prepare_test_data(test_inflections)
    
    # inlfect the test data
    predictions = inflect_data(test_lemmas, test_feature_descs, prefix_rule_collection, suffix_rule_collection)

    # output list for -l parameter
    if params["list"]:   
        for single_prediction in predictions:
            print(single_prediction) 
        print("")

    # output accuracy for given data
    if params["accuracy"]:
        correct, acc = compute_accuracy(predictions, test_ground_truth, verbose=False)    
        print("trained on: " + params["train"].split('/')[-1])
        print("- training instances: {}".format(len(train_inflections)))
        print("tested on: " + params["test"].split('/')[-1])
        print("- testing instances: {}".format(len(test_inflections)))
        print("- correct instances: {}".format(correct))
        print("- accuracy: {0:.3f}".format(acc * 100))

    return 0
    
if __name__ == "__main__":
    main()
