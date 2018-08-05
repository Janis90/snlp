import utils
from ChangingRule import SuffixRule, PrefixRule, RuleCollection
from UniMorph import UniMorph, FeatureCollection


def main():
    params = utils.read_params()
    
    # Create rules from training
    train_inflections = utils.read_file(params["train"])
    prefix_rule_collection, suffix_rule_collection = RuleCollection.create_rule_collections(train_inflections)

    # -- task 3 testing
    res_features = suffix_rule_collection.get_suitable_features("Abfall", "Abfall")
    print(res_features)


if __name__ == "__main__":
    main()
