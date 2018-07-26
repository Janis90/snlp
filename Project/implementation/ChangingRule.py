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

    def __str__(self):
        return "${} > ${}".format(self.input, self.output)

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
        empty_rule = SuffixRule("", "", inflection.inflection_desc_list)
        rules.append(empty_rule)

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
    def generate_rules(inflection):
        
        rules = []
        # generate and insert empty rule
        empty_rule = SuffixRule("", "", inflection.inflection_desc_list)
        rules.append(empty_rule)

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
