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

    def get_feature_intersection(self, feature_collection):
        """Returns a FeatureCollection instance only containing the features which are in this collectiona AND in the parameter feature collection
        
        Parameters
        ----------
        feature_collection : FeatureCollection
            FeatureCollection instance to intersect this collection with
        
        Returns
        -------
        FeatureCollection
            FeatureCollection instance after the intersection between this and the parameter's FeatureCollection instance
        """
        
        merged_collection = []

        for single_feature in self.features:
            if single_feature in feature_collection.features:
                merged_collection.append(single_feature)

        return FeatureCollection(merged_collection), len(merged_collection)

    def get_feature_union(self, feature_collection):
        """Returns a FeatureCollection instance containin all feature which are in this collection OR in the given FeatureCollection
        
        Parameters
        ----------
        feature_collection : FeatureCollection
            FeatureCollection instance to unify this feature collection with
        
        Returns
        -------
        FeatureCollection
            FeatureCollection instance containing all features from this and from the parameter's FeatureCollections.
        """
        
        merged_collection = self.features.union(feature_collection.features)
        return FeatureCollection(list(merged_collection)), len(merged_collection)



