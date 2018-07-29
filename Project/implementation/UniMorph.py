from aenum import Enum
import json
import numpy as np

# load data from .json file
with open('uniMorphSchema.json') as f:
    class_features = json.load(f)

# set all features into a single list
features = {}
for f_class, f_list in class_features.items():
    for single_f in f_list:
        features[single_f] = f_class

class UniMorph():

    def __init__(self, feature):

        self.feature = feature

        if feature not in features:
            print("WARNING: {} is not a valid UniMorph feature".format(feature))
            self.type = "UNKNOWN"
        else:
            self.type = features[feature]

    def __str__(self):
        return self.feature

    def __eq__(self, other):        
        if isinstance(other, UniMorph):
            return self.feature == other.feature
        return False

    @staticmethod
    def get_features(feature_list_string, separator=";"):

        feature_list = feature_list_string.split(separator)

        result_feature_list = []
        for single_feature in feature_list:
            new_feature = UniMorph(single_feature)
            result_feature_list.append(new_feature)

        return feature_list

class FeatureCollection():

    def __init__(self, feature_list):
        self.features = set(feature_list)

    @staticmethod
    def create_feature_collection(feature_list_string, separator=";"):
        feature_list = UniMorph.get_features(feature_list_string, separator=separator)
        return FeatureCollection(feature_list)

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, other):
        if isinstance(other, FeatureCollection):
            return self.features == other.features
        return False

    def __str__(self):
        res_str = ""

        for elem in self.features:
            res_str += str(elem) + ";"

        return res_str[:-1]





