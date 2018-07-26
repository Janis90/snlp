from Inflection import Inflection

class ChangingRule():
    """A ChaningRule describes the process of changing an input word with a certain strategy to an output. The 
    ChangingRule base class is virtual. Use PrefixRule or SuffixRule for application.
    """

    def __init__(self, str_in, str_out, inflection_desc_list):

        self.input = str_in
        self.output = str_out

        self.infection_desc = inflection_desc_list

    def apply_rule(self, lemma):
        """Applys this ChangingRule to a given string. If the rule does not match the word, the input word gets returned unchanged.
        
        Parameters
        ----------
        lemma : string
            Input word for which the rule should be applied
        
        """

        pass

    def get_overlap_score(self, word):
        """Returns the amount of characters in the input word which match the rule condition. Returns 0 if the rule does not
        match the condition and len(rule.input) otherwise.
        
        Parameters
        ----------
        word : string
            String for which the overlap score of this rule should be applied on.
        
        """
        pass

    @staticmethod
    def generate_rules(inflection):
        pass

    def is_applicable(self, word):

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
        rules.append(PrefixRule.empty_rule(inflection.inflection_desc_list))

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
        rules.append(SuffixRule.empty_rule(inflection.inflection_desc_list))

        rule_source = inflection.lemma.suffix
        rule_target = inflection.inflection.suffix

        new_rule = SuffixRule(rule_source, rule_target, inflection.inflection_desc_list)
        rules.append(new_rule)

        for i in reversed(range(len(list(inflection.lemma.stem)))):
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
            return len(self.input)
        else:
            return 0

    def __eq__(self, other):
        if isinstance(other, SuffixRule):
            return (self.input == other.input) and (self.output == other.output) and (self.infection_desc == other.infection_desc)
        return False

    def __hash__(self):
        return str(self).__hash__()


class RuleCollection():

    def __init__(self):
        self.rule_dict = {}

    def __str__(self):
        res_string = ""

        for feature_col, rule_dict in self.rule_dict.items():
            res_string += "\n{}:".format(feature_col)

            for rule_key, single_rule_dict in rule_dict.items():
                res_string += "\n\t{} - count: {}".format(single_rule_dict["rule"], single_rule_dict["count"])

        return res_string

    def add_rule(self, new_rule):
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

            if cur_count > highest_count:
                highest_count = cur_count
                best_rule = single_rule_dict["rule"]

        return best_rule

    def get_rules(self, inflection_desc):        
        return self.rule_dict.get(str(inflection_desc), [])

    @staticmethod
    def create_rule_collections(inflection_list):

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
