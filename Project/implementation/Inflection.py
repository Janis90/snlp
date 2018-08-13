import numpy as np
from implementation.Word import Word, LevinsteinPartition, KhalingXFixPartition
from aenum import Enum
 
class SplitMethod(Enum):
    LEVINSTEIN = 1
    KHALING_XFIX = 2


class Inflection():
    """An inflection consists of the infinitiv (Grundform) form of a word and its inflection (Beugung). Further
    an inflection object saves the inflection description features.
    """

    def __init__(self, lemma_word, inflection_word, inflection_desc_list):
        """Creating a new Inflection object
        
        Parameters:
        ------------
        lemma_word : Word object
            A word instance representing the lemma of the inflection.
        inflection_word : Word object
            A word instance representing the inflected lemma.
        inflection_desc_list :List<InflectionFeature>
            A list of uniMorph features describing this inflection.
        """
        
        self.lemma = lemma_word
        self.inflection = inflection_word

        self.inflection_desc_list = inflection_desc_list

    @staticmethod
    def create_inflection(lemma, inflection, inflection_desc_list, method=SplitMethod.KHALING_XFIX):
        """Creates an Inflectin object by two strings - one representing the lemma and the other one representing
        the inflection. The Inlfection gets created using levinstein distance.
        
        Parameters
        ----------
        lemma : string
            String representing lemma
        inflection : string
            String representing the inflected lemma
        inflection_desc_list : List<InflectionFeature>
            List of inlfection features describing the inflection
        
        Returns
        -------
        Inflection
            Inlfection object describing the inflection of the inputs
        """

        splitter = None

        if method == SplitMethod.LEVINSTEIN:
            splitter = LevinsteinPartition()   

        if method == SplitMethod.KHALING_XFIX:
            splitter = KhalingXFixPartition()
            
        lemma_word, inflection_word = splitter.split_word(lemma, inflection)

        return Inflection(lemma_word, inflection_word, inflection_desc_list)
