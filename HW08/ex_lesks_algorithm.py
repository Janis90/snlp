from nltk.corpus import stopwords
import utils


def sanitize(definition):
    stopword_list = set(stopwords.words('english'))
    def_1, def_2 = read_defintions(name)
    definition = utils.tokenize_text_string(definition,
                                            sanitize=True, remove_duplicates=True, stopwords=stop_words)

    definition = utils.lemma_stemming(definition, None, 'snowball')

    return definition


def read_defintions(name):
    lines = [line.rstrip('\n')
             for line in open("wsd_data/" + name + ".definitions")]

    return (lines[0], sanitize(lines[1])), (lines[2], sanitize(lines[3]))


def read_tests(name):
    lines = [line.rstrip('\n')
             for line in open("wsd_data/" + name + ".test")]

    result = []
    for idx, line in enumerate(lines):
        if line[0][0] == '#':

            result.append((line, sanitize(lines[idx + 1])))

    return result


def main():

    # ex 5
    bass_def = read_defintions('bass')
    bass_tests = read_tests('bass')

    crane_def = read_defintions('crane')
    crane_tests = read_tests('crane')

    motion_def = read_defintions('motion')
    motion_tests = read_tests('motion')

    palm_def = read_defintions('palm')
    palm_tests = read_tests('palm')

    plant_def = read_defintions('plant')
    plant_tests = read_tests('plant')

    tank_def = read_defintions('tank')
    tank_tests = read_tests('tank')


if __name__ == "__main__":
    main()
