import implementation.utils as utils
import numpy as np
from implementation.ChangingRule import SuffixRule, PrefixRule, ConditionalRule, RuleCollection
from implementation.UniMorph import UniMorph, FeatureCollection
from implementation.Inflection import SplitMethod

def compute_test_metrics(predictions, ground_truth):
    """Computes for a given list of predicted and expected FeatureCollections the Precision, Recall and F-Score rating.
    
    Parameters
    ----------
    predictions : List<FeatureColleciton>
        List of FeatureColleciton instances which contain the features that got predicted.
    ground_truth : List<FeatureColleciton>
        List of FeatureColleciton instances which contain the features that come from the test dataset representing the ground truth.
    
    Returns
    -------
    float, float, float
        Precision, Recall, F-Score
    """

    tp = 0
    fp = 0
    fn = 0
    
    # iterate over all instances
    for i in range(len(predictions)):

        for sinlge_feature in predictions[i].features:
            if sinlge_feature in ground_truth[i].features:
                # predicted feature is correct
                tp += 1
            else:
                # predicted feature is incorrect
                fp += 1

        for single_feature in ground_truth[i].features:
            if single_feature not in predictions[i].features:
                # feature in ground truth is missing in prediction
                fn += 1

    # computing the test metrics
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = (2 * precision * recall)/ (precision + recall)

    return precision, recall, f1


def compute_accuracy(predictions, ground_truth):
    """Computes the accuracy as well as the amount of true predicted instances
    
    Parameters
    ----------
    predictions : List<FeatureCollection>
        List of predicted feature collections
    ground_truth : List<FeatureCollection>
        List of expected feature collections
    
    Returns
    -------
    float, int
        Accuracy, amount of correctly predicted instances
    """


    true_predicted = 0
    
    # iterate over all instances
    for i in range(len(predictions)):

        if predictions[i] == ground_truth[i]:
            true_predicted += 1

    accuracy = true_predicted / len(predictions)

    return accuracy, true_predicted


def get_suitable_prefix_rules(lemma_str, inflection_str, rule_collection):
    """Returns a list of prefix rules from the RuleCollection instance which changes the lemma string in a way so that its beginning 
    equals to the one of the inflection string.
    
    Parameters
    ----------
    lemma_str : string
        Lemma string which gets manipulated. 
    inflection_str : string
        Resulting string how the lemma's beginning should look like after applying one of the suitable prefix rules
    rule_collection : RuleColleciton
        RuleCollection instance containing all prefix rules which should be checked to fit for the infection task
    
    Returns
    -------
    List<ChangingRules>
        A list of chaninging rules which change the lemma in a way so that the beginning equals to the one of the inflection string
    """

    suitable_rules = []

    # iterate over all rules
    for single_rule in rule_collection.get_rules():

        # check if the current rule is applicable to the lemma
        if single_rule.is_applicable(lemma_str):

            # apply the prefix tule to the lemma
            intermediate_inflection = single_rule.apply_rule(lemma_str)

            # check the amount of the changed characters
            rule_size = len(single_rule.output)

            # store rule if:
            # (1) The beginning of the changed lemma equals to the beginning of the inflection string
            # or (2) when the rule's output is empty, the first character of the lemma must equal to the first character of the inflection string
            if (rule_size > 0 and intermediate_inflection[:rule_size] == inflection_str[:rule_size]) or (rule_size == 0 and intermediate_inflection[0] == inflection_str[0]) :
                suitable_rules.append(single_rule)

    return suitable_rules


def get_suitable_suffix_rules(inter_inflection, inflection_str, rule_collection):
    """Returns a list of changing rules which, applied to the intermediate inflection return the inflection string.
    
    Parameters
    ----------
    inter_inflection : string
        the intermediate inflection is a lemma with applied prefix rule. After applying a suffix rule to it, this string should become the inflection
    inflection_str : string
        the target inflection string. If an intermediate inflection equals to this string after suffix rule application, the rule gets stored
    rule_collection : RuleCollection
        RuleCollection instance from which all rules get considered if they are suitable ChangingRules for this task
    
    Returns
    -------
    List<ChangingRule>
        List of SuffixRule instance, which all applied to the intermediate inflection become the inflection string.
    """

    suitable_rules = []

    # iterate over all rules of the collection
    for current_rule in rule_collection.get_rules():

        # check if the rule is applicable to the intermediate inflection
        if current_rule.is_applicable(inter_inflection):

            # apply the rule
            inflected_lemma = current_rule.apply_rule(inter_inflection)

            # compare inflection with expected result -  if equality holds, store the rule
            if inflected_lemma == inflection_str:
                suitable_rules.append(current_rule)

    return suitable_rules


def get_suitable_suffix_rules_soft(inflection_str, rule_collection):
    """Returns a list of suffix rules whith an output suiting to the inflection string parameter.
    
    Parameters
    ----------
    inflection_str : string
        inflection string whose end should equal to the selected suffix rule outputs
    rule_collection : RuleCollection
        RuleCollection instance from which all suffix rules should be checked to be suitable
    
    Returns
    -------
    List<ChangingRules>
        List of ChangingRule instances which all have an output which would fit to the inflection string 
    """

    suitable_rules = []

    # iterate over all rules in the collection
    for current_rule in rule_collection.get_rules():
        
        # the the length of the rule output
        out_len = len(current_rule.output)

        # check if the rule output fits to the ending of the inflection string, if it does, store the rule
        if current_rule.output == inflection_str[- out_len:]:
            suitable_rules.append(current_rule)

    return suitable_rules


def merge_rule_feautres(prefix_rule_list, suffix_rule_list, prefix_rule_col, suffix_rule_col):
    """Out of a list of prefix rules and a list of suffix rules, this method exctracts the features which are likely to fit the problem.
    First rule combinations are set up which provide a high overlap in features. From the rules with the highest overlaps, the union
    of all rule features will be returned.
    
    Parameters
    ----------
    prefix_rule_list : List<ChanginRule>
        List of all prefix rules which might contain the relevant features
    suffix_rule_list : List<ChangingRule>
        List of all suffix rules which might contain the relevant features
    prefix_rule_col : RuleCollection
        RuleCollection instance which contains all prefix rules, which should be considered
    suffix_rule_col : RuleCollection
        RuleColleciton sintacen which contains all suffix rules, which should be considered
    
    Returns
    -------
    FeatureCollection
        FeatureCollection instance which contains the combined features resulted from the application of the rule strategy
    """


    best_overlap = -1
    best_features = None

    combined_rule_data = []

    # consider all prefix suffix rule combinations
    for single_prefix_rule in prefix_rule_list:
        for single_suffix_rule in suffix_rule_list:

            # get the features which are present in both rules.
            intersect_features, overlap = single_prefix_rule.infection_desc.get_feature_intersection(single_suffix_rule.infection_desc)

            # append these features together with the rules and the overlap score
            combined_rule_data.append((single_prefix_rule, single_suffix_rule, intersect_features, overlap))

            # track and store the highest overlap score
            if overlap > best_overlap:
                best_overlap = overlap

    best_overlap_rules = []

    # only store the rules which achieved the highest overlap score
    for (prefix_rule, suffix_rule, int_features, overlap_val) in combined_rule_data:
        if overlap_val == best_overlap:
            best_overlap_rules.append((prefix_rule, suffix_rule, int_features, overlap_val))

    unified_features = set()
    
    # unify all features of the remaining feature collections with the same high overlap score
    for (prefix_rule, suffix_rule, int_features, overlap_val) in best_overlap_rules:
        unified_features = unified_features.union(int_features.features)

    # create and return one single feature collection instance out of the unified features
    best_features = FeatureCollection(list(unified_features))

    return best_features


def infer_inflection_features(lemma_str, inflection_str, prefix_rule_col, suffix_rule_col):
    """This funciton returns the feautres which are likely to describe the relation between the given lemma and the given inflection string
        
    Parameters
    ----------
    lemma_str : string
        string representing the lemma of a word
    inflection_str : string
        string representing the target inflection of the lemma
    prefix_rule_col : RuleCollection
        RuleCollection instance containing all prefix rules to be considered
    suffix_rule_col : RuleCollection
        RuleCollection instnance containing all suffix rules to be considered
    
    Returns
    -------
    FeatureCollection
        A single feature collection which represents the inference of the features form the lemma to the inflection
    """


    # get the prefix rules which suit the problem
    prefix_rule_candidates = get_suitable_prefix_rules(lemma_str, inflection_str, prefix_rule_col)

    # apply one of the prefix rules (all effects are the same) to the the intermediate inflection
    int_lemma = prefix_rule_candidates[0].apply_rule(lemma_str)

    # get the suffix rules which suit the problem with the intermediate inflection
    suffix_rule_candidates = get_suitable_suffix_rules(int_lemma, inflection_str, suffix_rule_col)

    # if we have no suitable suffix rules found
    if len(suffix_rule_candidates) == 0:
        
        # use the rules which only fits by their output
        soft_rules = get_suitable_suffix_rules_soft(inflection_str, suffix_rule_col)
        suffix_rule_candidates = soft_rules

    # if we have no suitable prefix rules have been found, just use the suffix rules for merging
    if len(prefix_rule_candidates) == 0:
        prefix_rule_candidates = suffix_rule_candidates
       

    # merge together all features to get the most likely features from all related rules
    best_features = merge_rule_feautres(prefix_rule_candidates, suffix_rule_candidates, prefix_rule_col, suffix_rule_col)

    return best_features


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


def main():

    # read parameters from CLI
    params = utils.read_params()
    
    # Create rules from training
    train_inflections = utils.read_file(params["train"], split_method=SplitMethod.KHALING_XFIX)
    prefix_rule_collection, suffix_rule_collection = RuleCollection.create_rule_collections(train_inflections)

    # create rules from test set
    test_inflections = utils.read_file(params["test"], split_method=SplitMethod.KHALING_XFIX)
    test_lemmas, test_feature_descs, test_inflection = prepare_test_data(test_inflections)

    predicted_feature_descriptions = []

    # iterate over all instances of the test set
    for i in range(len(test_lemmas)):

        # extract current lemma and the current target inflection
        cur_lemma = test_lemmas[i]
        cur_inflection = test_inflection[i]

        # infer the features to the current data
        pred_features = infer_inflection_features(cur_lemma, cur_inflection, prefix_rule_collection, suffix_rule_collection)
        
        # if no features have been found, use an empty feature collection
        if pred_features is None:
            pred_features = FeatureCollection([])

        # store the current result
        predicted_feature_descriptions.append(pred_features)

     # output list for -l parameter
    if params["list"]:   
        for single_prediction in predicted_feature_descriptions:
            print(single_prediction) 
        print("")

    # output accuracy for given data
    if params["accuracy"]:
        acc, correct = compute_accuracy(predicted_feature_descriptions, test_feature_descs)    

        print("trained on: " + params["train"].split('/')[-1])
        print("- training instances: {}".format(len(train_inflections)))
        print("tested on: " + params["test"].split('/')[-1])
        print("- testing instances: {}".format(len(test_inflections)))
        print("- correct instances: {}".format(correct))
        print("- accuracy: {0:.3f}".format(acc * 100))


    # # compute the test metrics from the results
    # prec, rec, f1 = compute_test_metrics(predicted_feature_descriptions, test_feature_descs)
    # print("\n\nRESULTS:\n Precision: {}\n Recall: {} \n F1-SCORE: {}".format(prec, rec, f1))

if __name__ == "__main__":
    main()
