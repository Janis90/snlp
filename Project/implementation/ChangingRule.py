from Inflection import Inflection

class ChangingRule():
    """A general ChaningRule describes the process of changing an input word with a certain strategy to an output. The 
    ChangingRule base class refers to replacing a certain part of an input. PrefixRule or SuffixRule are applied for changes at the 
    referring position.
    """

    def __init__(self, str_in, str_out, inflection_desc_list=None):

        self.input = str_in
        self.output = str_out
        self.infection_desc = inflection_desc_list

    def apply_rule(self, lemma):
        """Applys this ChangingRule to a given string. If the rule does not match the word, the input word gets returned unchanged.
        
        Parameters
        ----------
        lemma : string
            Input word for which the rule should be applied

        Returns
        -------
        string
            The lemma string after the applied rule
        """
        return lemma.replace(self.input, self.output)

    def get_overlap_score(self, word):
        """Returns the amount of characters in the input word which match the rule condition. Returns 0 if the rule does not
        match the condition and len(rule.input) otherwise.
        
        Parameters
        ----------
        word : string
            String for which the overlap score of this rule should be applied on.
        
        """
        if self.input in word:
            return len(self.input)
        else:
            return 0

    @staticmethod
    def generate_rules(inflection):
        print("A general ChangingRule cannot be created from an inflection. Use Prefix or Suffix rules")
        raise NotImplementedError

    def is_applicable(self, word):
        """Checks if this rule can be applied to a given word string i.e. wheather the rule input matches with the given word.
        
        Parameters
        ----------
        word : string
            Word for which the rule application should be checked
        
        Returns
        -------
        bool
            True if the rule is applicable, else False
        """

        if self.input == "":
            return True
        else:
            return self.get_overlap_score(word) > 0

    def __str__(self):
        return "{}$ > {}$".format(self.input, self.output)

    def __hash__(self):
        return str(self).__hash__()

    
class PrefixRule(ChangingRule):
    """A PrefixRule describes the process of changing the prefix of a word with a certain strategy.
    
    Inherits from
    ----------
    ChangingRule
    """

    def __init__(self, str_in, str_out, inflection_desc_list):
        """A PrefixRule replaces the input prefix with a defined prefix. To create a PrefixRule out of a lemma and an inflection
        use generate_rules()
        
        Parameters
        ----------
        str_in : string
            prefix string that should exist in the uninflected word
        str_out : string
            prefix string which replaces the prefix in order to perform an inflection
        inflection_desc_list : List<InflectionFeature>
            List of uniMorph features describing the inflection process
        
        """

        super().__init__(str_in, str_out, inflection_desc_list)

        # counter for the occurrences of this rule
        self.count = 1

    def __str__(self):
        return "${} > ${}".format(self.input, self.output)

    @staticmethod
    def empty_rule(inflection_desc_list):
        """Simple instance of an empty PrefixRule
        
        Parameters
        ----------
        inflection_desc_list : PrefixRule
        
        Returns
        -------
        PrefixRule
            
        """

        return PrefixRule("", "", inflection_desc_list)

    @staticmethod
    def generate_rules(inflection):
        """Generates a list of inflection rules out of a lemma Word and an inflection Word.
        
        Parameters
        ----------
        lemma : Word
            A Word instance of the lemma.
        inflection : Word
            A Word instance of the inflected lemma. 
        inflection_desc_list : List<InflectionFeatures>
            A list of uniMorph features describing the inflection process
        
        Returns
        -------
        List<PrefixRule>
            A list of PrefixRules which can be generated out the the lemma-inflection relation.
        """

        rules = []

        # TODO: Usually we get the empty rule as most common rule :(
        # --> leaving this out is required instead empty rule is always most dominant
        # rules.append(PrefixRule.empty_rule(inflection.inflection_desc_list))

        rule = PrefixRule(inflection.lemma.prefix, inflection.inflection.prefix, inflection.inflection_desc_list)
        rules.append(rule)
        return rules

    def apply_rule(self, lemma):
        result = "$" + lemma
        
        if "$" + self.input in result:
            result = result.replace("$" + self.input, self.output)
            return result
        else:
            return lemma

    def get_overlap_score(self, word):
        input_word = "$" + word
        if "$" + self.input in input_word:
            return len(self.input)
        else:
            return 0

    def __eq__(self, other):
        if isinstance(other, PrefixRule):
            return (self.input == other.input) and (self.output == other.output) and (self.infection_desc == other.infection_desc)
        return False

    def __hash__(self):
        return str(self).__hash__()

class SuffixRule(ChangingRule):

    def __init__(self, str_in, str_out, inflection_desc_list):
        super().__init__(str_in, str_out, inflection_desc_list)

    @staticmethod
    def empty_rule(inflection_desc_list):
        return SuffixRule("", "", inflection_desc_list)

    @staticmethod
    def generate_rules(inflection):
        
        rules = []
        # generate and insert empty rule
        # rules.append(SuffixRule.empty_rule(inflection.inflection_desc_list))

        rule_source = inflection.lemma.suffix
        rule_target = inflection.inflection.suffix

        new_rule = SuffixRule(rule_source, rule_target, inflection.inflection_desc_list)
        rules.append(new_rule)

        # TODO: problem when source and target stem have different lengths
        for i in reversed(range(len(list(inflection.lemma.stem)))):

            if len(inflection.lemma.stem) <= i or len(inflection.inflection.stem) <= i:
                break

            print("i: {}, lemma stem: {}, inflectin stem: {}".format(i, len(inflection.lemma.stem), len(inflection.inflection.stem)))
            rule_source = inflection.lemma.stem[i] + rule_source
            rule_target = inflection.inflection.stem[i] + rule_target
            new_rule = SuffixRule(rule_source, rule_target, inflection.inflection_desc_list)
            rules.append(new_rule)

        return rules

    def apply_rule(self, lemma):
        result = lemma + "$"
        
        if self.input + "$" in result:
            result = result.replace(self.input + "$", self.output)
            return result
        else:
            return lemma

    def get_overlap_score(self, word):
        input_word = word + "$"
        if self.input + "$" in input_word:

            # if rule contains whole word
            if len(self.input) == len(word):
                return 0

            return len(self.input)
        else:
            return 0

    def __eq__(self, other):
        if isinstance(other, SuffixRule):
            return (self.input == other.input) and (self.output == other.output) and (self.infection_desc == other.infection_desc)
        return False

    def __hash__(self):
        return str(self).__hash__()

class ConditionalRule(ChangingRule):

    def __init__(self, str_in, str_out, inflection_desc_list=None, condition_function=None):
        super().__init__(str_in, str_out, inflection_desc_list)

        self.condition_function = condition_function

    def apply_rule(self, lemma):

        if self.condition_function is not None:
            if self.condition_function(self, lemma):
                return lemma.replace(self.input, self.output)
            else:
                return lemma
        else:
            return lemma.replace(self.input, self.output)

    def get_overlap_score(self, word):

        if self.condition_function is not None:
            if self.condition_function(self, word):
                if self.input in word:
                    return len(self.input)
        
        return 0

    def is_applicable(self, word):

        if self.condition_function is None:
            if self.input == "":
                return True
            else:
                return self.get_overlap_score(word) > 0
        else:
            if self.condition_function(self, word):
                if self.input == "":
                    return True
                else:
                    return self.get_overlap_score(word) > 0

            else:
                return False

    def __str__(self):
        return "{}$ > {}$ (conditional)".format(self.input, self.output)

class RuleCollection():
    """A RuleCollection instance stores and manages multiple chagning rules which could result from a training procedure.
    """
    def __init__(self):
        """Creates an empty RuleCollection instance. To create a rule collection given a list of Inflections use create_rule_collections()
        
        """
        self.rule_dict = {}

    def __str__(self):
        res_string = ""

        for feature_col, rule_dict in self.rule_dict.items():
            res_string += "\n{}:".format(feature_col)

            for rule_key, single_rule_dict in rule_dict.items():
                res_string += "\n\t{} - count: {}".format(single_rule_dict["rule"], single_rule_dict["count"])

        return res_string

    def add_rule(self, new_rule):
        """Adds a single ChangingRule instance to the collection.
        
        Parameters
        ----------
        new_rule : ChangingRule
            The ChangingRule instance to add
        
        """

        feature_list = new_rule.infection_desc

        if str(feature_list) in self.rule_dict:
            if str(new_rule) in self.rule_dict[str(feature_list)]:
                # increase count
                self.rule_dict[str(feature_list)][str(new_rule)]["count"] += 1
            else:
                # add rule
                self.rule_dict[str(feature_list)][str(new_rule)] = {"rule": new_rule, "count": 1}
        else:
            self.rule_dict[str(feature_list)] = {str(new_rule): {"rule": new_rule, "count": 1}}
                
    def get_highest_overlap_rule(self, input_str, inflection_desc):
        """Returns a single ChangingRule from this collection which provides the highest overlap for a given word string and a 
        corresponding infelction feature collection. If multiple rules have the same overlap scoring, this methods returns the
        rule which appeard as most frequent in the training.
        
        Parameters
        ----------
        input_str : string
            Input word string (usually an infinitiv) for which a ChaningRule should be found.
        inflection_desc : FeatureCollection
            A collection for inflection features which describe the whiched inflection process.
        
        Returns
        -------
        ChangingRule
            The most suitable ChanginRule instance from this collection which (1) fits to the given string, (2) provides the highest
            overlap to the input string and (3) is the most frequent among all other rules with the same overlap score.
        """

        # if feature combination did not appear in rule collection
        if str(inflection_desc) not in self.rule_dict:
            return None

        highest_score = 0
        best_rules = []

        for single_rule_dict in self.rule_dict[str(inflection_desc)].values():
            overlap_score = single_rule_dict["rule"].get_overlap_score(input_str)

            if overlap_score > highest_score:
                highest_score = overlap_score
                best_rules = [single_rule_dict]
            elif overlap_score == highest_score:
                best_rules.append(single_rule_dict)

        # TODO: Not sure if we really want this, but otherwise results are quite random for many cases
        # among all possible rules take the most frequent one
        highest_count = 0
        best_rule = None

        # get rules with highest frequency
        for single_rule_dict in best_rules:
                
            # if rule does not match to word
            if not single_rule_dict["rule"].is_applicable(input_str):
                continue            

            cur_count = single_rule_dict["count"]

            if cur_count > highest_count:
                highest_count = cur_count
                best_rule = single_rule_dict["rule"]

        return best_rule

    def get_highest_count_rule(self, input_str, inflection_desc):
        """Returns the ChanginRule instance of this collection which (1) is applicable for the given inflection feature description,
        (2) fits for a given input string and (3) appeard most frequent during the training stage.
        
        Parameters
        ----------
        input_str : string
            Input string (usually infinitiv) for which the suitable ChanginRule should be found
        inflection_desc : FeatureCollection
            A FeatureCollection instance describing the inflection process.
        
        Returns
        -------
        ChangingRule
            The most suitable ChanginRule instance
        """


         # if feature combination did not appear in rule collection
        if str(inflection_desc) not in self.rule_dict:
            return None
        
        highest_count = 0
        best_rule = None

        for single_rule_dict in self.rule_dict[str(inflection_desc)].values():

            # if rule does not match to word
            if not single_rule_dict["rule"].is_applicable(input_str):
                continue            

            cur_count = single_rule_dict["count"]
            # print("Rule: {} Count: {}".format(single_rule_dict["rule"], cur_count))

            if cur_count > highest_count:
                highest_count = cur_count
                best_rule = single_rule_dict["rule"]

        return best_rule

    def get_rules(self, inflection_desc):     
        """Returns a list of ChangingRule from this collection which fit for a given FeatureCollection. This method is thought for debugging.
        
        Parameters
        ----------
        inflection_desc : FeatureCollection
            A FeatureCollection instance for which the ChangingRules of this collection should be filtered
        
        Returns
        -------
        Dict<{str(ChanginRule): {"rule": ChanginRule, "count": int}}>
            A dictionary containing all applicable ChaningRules for the given FeatureCollection
        """

        return self.rule_dict.get(str(inflection_desc), [])

    @staticmethod
    def create_rule_collections(inflection_list):
        """Creates two instances of RuleCollections out of a list of Inflection instances - one for prefix rules and one for suffix rules.
        For each Inflection first, the SuffixRules get extracted and packed into a RuleCollection instance; afterwards the same happens
        for PrefixRules.
        
        Parameters
        ----------
        inflection_list : List<Inflection>
            A list of Inflection instances for which the pre- and suffix rules should be extracted.
        
        Returns
        -------
        RuleCollection, RuleCollection
            First an instance of a RuleCollection containing all PrefixRules and a RuleCollection withe the extractes SuffixRules.
        """


        prefix_rule_collection = RuleCollection()
        suffix_rule_collection = RuleCollection()

        for inflection in inflection_list:

            # First the suffix changing rules          
            suffix_rules = SuffixRule.generate_rules(inflection)

            for rule in suffix_rules:
                suffix_rule_collection.add_rule(rule)

            # Then the prefix changing rules
            prefix_rules = PrefixRule.generate_rules(inflection)

            for rule in prefix_rules:
                prefix_rule_collection.add_rule(rule)

        return prefix_rule_collection, suffix_rule_collection

    def get_suitable_features(self, lemma_str, inflection_str):
        """This method searches the most suitable rule which applied to the lemma_str provides the given inflection_str as output.
        If multiple rules return the same correct inflection, the rule with the highest overlap and then with the highest count
        is returned.
        
        Parameters
        ----------
        lemma_str : string
            lemma of the word which should be inflected
        inflection_str : string
            inflected lemma string
        
        Returns
        -------
        FeatureCollection
            The FeatureCollection instance of the most suitable rule. None if no rule could reproduce the requtested output
        """

        candidate_rules = []

        # iterate over all rules
        for feature_list, rule_data in self.rule_dict.items():
            for rule_rep, single_rule in rule_data.items():
                current_rule = single_rule["rule"]

                # check wheather rule can be applied
                if current_rule.is_applicable(lemma_str):

                    # compute the inflection
                    inflected_lemma = current_rule.apply_rule(lemma_str)

                    # compare inflection with expected result
                    if inflected_lemma == inflection_str:
                        candidate_rules.append(single_rule)
                        
        if len(candidate_rules) == 0:
            return

        # out of a list of possible rules choose the with the highest overlap and than with the highest count

        # compute the overlap score for all candidates and store the highest score
        highest_overlap = 0
        for single_rule in candidate_rules:
            ov_score = single_rule["rule"].get_overlap_score(lemma_str)
            single_rule["overlap"] = ov_score#

            if ov_score > highest_overlap:
                highest_overlap = ov_score

        # filter out rules with a lower overlap score than the highest
        filtered_candidate_rules = []
        for single_rule in candidate_rules:
            if single_rule["overlap"] == highest_overlap:
                filtered_candidate_rules.append(single_rule)

        # among the remaining rules, choose the one with the highest count
        best_rule = filtered_candidate_rules[0]

        for single_candidate in filtered_candidate_rules:
            if single_candidate["count"] > best_rule["count"]:
                best_rule = single_candidate

        # print("rule: {}, overlap: {}, count: {}".format(best_rule["rule"], best_rule["overlap"], best_rule["count"]))

        # return the feature list of the best rule
        return best_rule["rule"].infection_desc

    def try_and_apply_all(self, input_str):

        for inflection_desc, single_rule_dict in self.rule_dict.items():
            for single_rule_name, rule_data in single_rule_dict.items():

                cur_rule = rule_data["rule"]

                if cur_rule.is_applicable:
                    input_str = cur_rule.apply_rule(input_str)

        return input_str



if __name__ == "__main__":

    # Example using ChangingRules
    # Using Inflection Objects
    lemma = "schielen"
    inflect = "geschielt"
    feature_list = []

    # create inflection object managing prefix, stem, suffix by levinstein
    inflect_obj = Inflection.create_inflection(lemma, inflect, feature_list)

    # create rules by only observing stem and suffix
    suffix_rules = SuffixRule.generate_rules(inflect_obj, feature_list)

    # print all suffix rules form the generation
    for rule in suffix_rules:
        print(rule)

    # create prefix rules by only observing prefix
    prefix_rules = PrefixRule.generate_rules(inflect_obj, feature_list)
    for rule in prefix_rules:
        print(rule)

    # example applying rule 2 (en -> t) to word "verkaufen"
    applied_rule = suffix_rules[2].apply_rule("verkaufen")
    print(applied_rule)

    # example for the overlap score
    overlap = suffix_rules[2].get_overlap_score("verkaufen")
    print(overlap)
