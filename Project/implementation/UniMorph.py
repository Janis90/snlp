from aenum import Enum
import json
import numpy as np

# load data from .json file
with open('implementation/uniMorphSchema.json') as f:
    class_features = json.load(f)

# set all features into a single list
features = {}
for f_class, f_list in class_features.items():
    for single_f in f_list:
        features[single_f] = f_class

class UniMorph():
    """The UniMorph class handles the UniMorph feature descriptions for inflections. All UniMorph labels are organized in uniMorphSchema.json
    """


    def __init__(self, feature, give_warning=True):
        """Creates a new UniMorph feature object. If the object is not listed in the .json file, a warning text will be displayed
        
        Parameters
        ----------
        feature : string
            UniMorph feature wirtten as string
        
        """


        self.feature = feature

        if feature not in features:
            if give_warning:
                print("WARNING: {} is not a valid UniMorph feature".format(feature))
            self.type = "UNKNOWN"
        else:
            self.type = features[feature]

    def __str__(self):
        return self.feature

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, other):        
        if isinstance(other, UniMorph):
            return self.feature == other.feature
        return False

    @staticmethod
    def get_features(feature_list_string, separator=";"):
        """Creates a list of UniMorph features out of a string with semicolon separated UniMorph feature strings.
        
        Parameters
        ----------
        feature_list_string : string
            separated uni morph feature strings
        separator : str, optional
            separator symbol of the feautre strings (the default is ";")
        
        Returns
        -------
        List<UniMorph>
        """


        feature_list = feature_list_string.split(separator)

        result_feature_list = []
        for single_feature in feature_list:
            new_feature = UniMorph(single_feature)
            result_feature_list.append(new_feature)

        return result_feature_list

class FeatureCollection():
    """A feature collection is a representation of a list of UniMorph features. To guarantee uniquness and equality measure for feature
    lists, use this class instead of List<UniMorph>
    """


    def __init__(self, feature_list):
        """Creates a FeatureCollection instance out of a list of UniMorp features
        
        Parameters
        ----------
        feature_list : List<UniMorph>
            List of UniMorph features that should set up this collection
        
        """

        self.features = set(feature_list)

    @staticmethod
    def create_feature_collection(feature_list_string, separator=";"):
        """Creates a FeatureCollection instance out of a string of UniMorph features. Use this method for parsing features.
        
        Parameters
        ----------
        feature_list_string : string
            String containing the UniMorph features. E.g. "V;PST;NEG;3;DU"
        separator : str, optional
            String separator between single features (the default is ";")
        
        Returns
        -------
        FeatureCollection
            A FeatureCollection instance containing all extracted features
        """

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

    def merge_with_collection1(self, feature_collection):

        merged_collection = None
        overlap = 0

        type_dict = {}

        # sort features from this feature collection
        for single_feature in self.features:
            # TODO: person/unkonwn can have multiple entries
            
            if single_feature.type == "UNKNOWN" or single_feature.type == "Person":
                continue

            if single_feature.type in type_dict:
                type_dict[single_feature.type].append(single_feature)
                print("Dimension: {}".format(single_feature.type))
                for i in type_dict[single_feature.type]:
                    print(i)
                assert False
                type_dict[single_feature.type].append(single_feature)
            else: 
                type_dict[single_feature.type] = [single_feature]

        # sort in features from the other feature collection
        for single_feature in feature_collection.features:
            if single_feature.type in type_dict:

                if single_feature in type_dict[single_feature.type]:
                    overlap += 1
                else:
                    # could here return None, 0
                    type_dict[single_feature.type].append(single_feature)

            else: 
                type_dict[single_feature.type] = [single_feature]

        final_features = []

        for feature_type, feature_set in type_dict.items():

            if len(feature_set) > 1:
                return None, 0

            final_features.append(feature_set[0])

        merged_collection = FeatureCollection(final_features)

        return merged_collection, overlap

    def merge_with_collection2(self, feature_collection):
        
        merged_collection = []

        for single_feature in self.features:
            if single_feature in feature_collection.features:
                merged_collection.append(single_feature)

        return FeatureCollection(merged_collection), len(merged_collection)

    def merge_with_collection(self, feature_collection):
        
        merged_collection = self.features.union(feature_collection.features)

        return FeatureCollection(list(merged_collection)), len(merged_collection)



