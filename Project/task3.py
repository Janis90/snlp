import implementation.utils as utils
import numpy as np
from implementation.ChangingRule import SuffixRule, PrefixRule, ConditionalRule, RuleCollection
from implementation.UniMorph import UniMorph, FeatureCollection
from implementation.Inflection import SplitMethod

def compute_test_metrics(predictions, gt):

    tp = 0
    fp = 0
    fn = 0

    for i in range(len(predictions)):

        for sinlge_feature in predictions[i].features:
            
            if sinlge_feature in gt[i].features:
                tp += 1
            else:
                fp += 1

        for single_feature in gt[i].features:
            if single_feature not in predictions[i].features:
                fn += 1

        print(predictions[i], gt[i], tp, fp, fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = (2 * precision * recall)/ (precision + recall)

    return precision, recall, f1

def get_suitable_prefix_rules(lemma_str, inflection_str, rule_collection):

    suitable_rules = []

    for single_rule in rule_collection.get_rules():

        if single_rule.is_applicable(lemma_str):
            intermediate_inflection = single_rule.apply_rule(lemma_str)

            rule_size = len(single_rule.output)

            if (rule_size > 0 and intermediate_inflection[:rule_size] == inflection_str[:rule_size]) or (rule_size == 0 and intermediate_inflection[0] == inflection_str[0]) :
                suitable_rules.append(single_rule)

    return suitable_rules

def get_suitable_suffix_rules(inter_inflection, inflection_str, rule_collection):

    suitable_rules = []

    for current_rule in rule_collection.get_rules():

        if current_rule.is_applicable(inter_inflection):

            # compute the inflection
            inflected_lemma = current_rule.apply_rule(inter_inflection)

            # compare inflection with expected result
            if inflected_lemma == inflection_str:
                suitable_rules.append(current_rule)

    return suitable_rules

def get_suitable_suffix_rules_soft(inflection_str, rule_collection):
    suitable_rules = []

    for current_rule in rule_collection.get_rules():
        
        out_len = len(current_rule.output)
        if current_rule.output == inflection_str[- out_len:]:
            suitable_rules.append(current_rule)

    return suitable_rules


def merge_rule_feautres(rule_list_1, rule_list_2, prefix_rule_col, suffix_rule_col):

    best_overlap = -1
    best_features = None

    dbg_list = []

    for single_rule_1 in rule_list_1:
        for single_rule_2 in rule_list_2:
            merging, overlap = single_rule_1.infection_desc.merge_with_collection2(single_rule_2.infection_desc)

            dbg_list.append((single_rule_1, single_rule_2, merging, overlap))

            if overlap > best_overlap:
                best_overlap = overlap
                best_features = merging

    overlaps = 0

    best_overlap_rules = []


    # print("Rules with same overlap:")
    for (r1, r2, m, ovl) in dbg_list:
        if ovl == best_overlap:
            overlaps += 1
            best_overlap_rules.append((r1, r2, m, ovl))
            # print("Rule1: {} - {} Rule2: {} - {} | Merge: {}".format(r1, r1.infection_desc, r2, r2.infection_desc, m))

    best_count = -1
    # best_rule = None
    unified_features = set()
    
    for (r1, r2, m, ovl) in best_overlap_rules:
        # prefix_count = prefix_rule_col.get_rule_count(r1)
        # suffix_count = suffix_rule_col.get_rule_count(r2)

        unified_features = unified_features.union(m.features)

        # cur_count = prefix_count + suffix_count

        # if best_count < cur_count:
        #     best_count = cur_count
        #     best_features = m
    best_features = FeatureCollection(list(unified_features))
    return best_features


def infer_inflection_features(lemma_str, inflection_str, prefix_rule_col, suffix_rule_col):

    prefix_rule_candidates = get_suitable_prefix_rules(lemma_str, inflection_str, prefix_rule_col)

    # print("Prefix Rules")
    # for i in prefix_rule_candidates:
        # print("Rule: {} - {}".format(i, i.infection_desc))
    
    int_lemma = prefix_rule_candidates[0].apply_rule(lemma_str)

    suffix_rule_candidates = get_suitable_suffix_rules(int_lemma, inflection_str, suffix_rule_col)

    if len(prefix_rule_candidates) == 0:
        return suffix_rule_candidates[0]

    # print("Suffix Rules")
    # for i in suffix_rule_candidates:
        # print("Rule: {} - {}".format(i, i.infection_desc))

    if len(suffix_rule_candidates) == 0:
        # print("\n-- no suffix rules fount\n")

        soft_rules = get_suitable_suffix_rules_soft(inflection_str, suffix_rule_col)
        # print("Soft Rules")
        suffix_rule_candidates = soft_rules
        # for r1 in soft_rules:
            # print("Rule: {} - {}".format(r1, r1.infection_desc))
        # return prefix_rule_candidates[0]

    best_features = merge_rule_feautres(prefix_rule_candidates, suffix_rule_candidates, prefix_rule_col, suffix_rule_col)

    # if best_features is None:
    #     print("\n no merging possible")
    #     return FeatureCollection([])

    # print("\n best features: {}".format(best_features))
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

    for i in range(len(test_lemmas)):
        cur_lemma = test_lemmas[i]
        cur_inflection = test_inflection[i]

        pred_features = infer_inflection_features(cur_lemma, cur_inflection, prefix_rule_collection, suffix_rule_collection)
        if pred_features is not None:
            predicted_feature_descriptions.append(pred_features)

        print("Lemma: {} Inflection: {} Features: {} Prediction: {}".format(cur_lemma, cur_inflection, test_feature_descs[i], pred_features))

    prec, rec, f1 = compute_test_metrics(predicted_feature_descriptions, test_feature_descs)
    print("\n\nRESULTS:\n Precision: {}\n RECALL: {} \n F1-SCORE: {}".format(prec, rec, f1))

    # eye debugging
    # for i in range(len(test_feature_descs)):
    #     print("predicted: {}\t\texpected: {}\t\t{}".format(predicted_feature_descriptions[i], test_feature_descs[i], predicted_feature_descriptions[i] == test_feature_descs[i]))



if __name__ == "__main__":
    main()
