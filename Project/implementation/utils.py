import argparse
import sys
import implementation.Inflection
from implementation.UniMorph import UniMorph, FeatureCollection
from implementation.Inflection import SplitMethod


def read_params():
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--group", required=False, action='store_true',
                    help="Print your group informations and exit")
    ap.add_argument("-tr", "--train", required=False, default=None,
                    help="Path to the trainings file")
    ap.add_argument("-te", "--test", required=False, default=None,
                    help="Path to the test file")
    ap.add_argument("-a", "--accuracy", required=False, action='store_true', default=None,
                    help="Your system prints the accuracy following the format given before. This is only called with 3-column test files")

    ap.add_argument("-l", "--list", required=False, action='store_true', default=None,
                    help="Your system prints each generated target form (Tasks 1,2) or inflection feature bundle (Task 3) to the standard output with one instance per line")

    args = vars(ap.parse_args())

    if args['group']:
        print_members()

    validate_args(args, ap)

    return args


def print_members():
    members = """
Group L06: Khaling
Janis Landwehr, 2547715, s9jaland@stud.uni-saarland.de
Sven Stauden, 2549696, s9svstau@stud.uni-saarland.de
Carsten Klaus, 2554140, s8caklau@stud.uni-saarland.de
"""
    print(members)
    sys.exit()


def validate_args(args, ap):
    path_count = len(
        [x for x in (args['train'], args['test']) if x is not None])

    if not (args['accuracy'] or args['list']):
        ap.error('--list or --accuracy need to be specified')
    else: 
        if not (args['test']): 
            ap.error('--test must be given for evaluation')

    if path_count == 0:
        ap.error('--tr and --te need to be specified')


    if path_count == 1:
        ap.error('--tr and --te must be given together')


def read_file(path, split_method=SplitMethod.LEVINSTEIN):
    """Reads a text file containing inflection samples of shape <inflection> <infinitiv> <inflection features>. For each line of the
    file, this methods creates an inflection instance and stores all together in a list.
    
    Parameters
    ----------
    path : string
        path to the text file to read
    
    Returns
    -------
    List<Inflection>
        A list containing all inflection instances extracted from the text file
    """

    input = open(path, encoding="utf8")

    inflections = []

    for instance in input:
        lemma, inflection, feature_list_str = instance.split()

        feature_col = FeatureCollection.create_feature_collection(feature_list_str)

        new_inflection = implementation.Inflection.Inflection.create_inflection(lemma, inflection, feature_col, method=split_method)
        inflections.append(new_inflection)

    return inflections
