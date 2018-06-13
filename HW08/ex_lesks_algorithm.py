from nltk.corpus import stopwords
import utils


def sanitize(definition):
    stopword_list = set(stopwords.words('english'))
    definition = utils.tokenize_text_string(definition,
                                            sanitize=True, remove_duplicates=True, stopwords=stopword_list)

    definition = utils.lemma_stemming(definition, None, 'snowball')

    return definition


def read_defintions(name):
    lines = [line.rstrip('\n')
             for line in open("./wsd_data/" + name + ".definition") if line.rstrip('\n') != ""]

    return [(lines[0][12:], sanitize(lines[1])), (lines[2][12:], sanitize(lines[3]))]


def read_tests(name):
    lines = [line.rstrip('\n')
             for line in open("./wsd_data/" + name + ".test") if line.rstrip('\n') != ""]
    result = []
    for idx, line in enumerate(lines):
        if line[0] == '#':
            result.append((line[7:], sanitize(lines[idx + 1])))

    return result


def calc_most_frequent_sense(defs, tests):
    total_right = 0

    for test in tests:
        result = defs[0][0]

        if result == test[0]:
            total_right += 1
            # print('correctly classified as ' + test[0])
        # else:
            # print('should have been ' + test[0])

    print('Accuracy most frequent sense ' +
          str(total_right / float(len(tests))))


def run_lesks_algorithm(defs, tests, type):
    total_right = 0

    for test in tests:
        result = utils.lesks_algorithm(defs, test, type)

        if result == test[0]:
            total_right += 1
            # print('correctly classified as ' + test[0])
        # else:
            # print('should have been ' + test[0])

    print('Accuracy (' + type + ') ' + str(total_right / float(len(tests))))


def main():

    # ex 5
    bass_defs = read_defintions('bass')
    bass_tests = read_tests('bass')
    print('bass')
    run_lesks_algorithm(bass_defs, bass_tests, 'default')
    calc_most_frequent_sense(bass_defs, bass_tests)
    run_lesks_algorithm(bass_defs, bass_tests, 'jaccards')

    crane_defs = read_defintions('crane')
    crane_tests = read_tests('crane')
    print('crane')
    run_lesks_algorithm(crane_defs, crane_tests, 'default')
    calc_most_frequent_sense(crane_defs, crane_tests)
    run_lesks_algorithm(crane_defs, crane_tests, 'jaccards')

    motion_defs = read_defintions('motion')
    motion_tests = read_tests('motion')
    print('motion')
    run_lesks_algorithm(motion_defs, motion_tests, 'default')
    calc_most_frequent_sense(motion_defs, motion_tests)
    run_lesks_algorithm(motion_defs, motion_tests, 'jaccards')

    palm_defs = read_defintions('palm')
    palm_tests = read_tests('palm')
    print('palm')
    run_lesks_algorithm(palm_defs, palm_tests, 'default')
    calc_most_frequent_sense(palm_defs, palm_tests)
    run_lesks_algorithm(palm_defs, palm_tests, 'jaccards')

    plant_defs = read_defintions('plant')
    plant_tests = read_tests('plant')
    print('plant')
    run_lesks_algorithm(plant_defs, plant_tests, 'default')
    calc_most_frequent_sense(plant_defs, plant_tests)
    run_lesks_algorithm(plant_defs, plant_tests, 'jaccards')

    tank_defs = read_defintions('tank')
    tank_tests = read_tests('tank')
    print('tank')
    run_lesks_algorithm(tank_defs, tank_tests, 'default')
    calc_most_frequent_sense(tank_defs, tank_tests)
    run_lesks_algorithm(tank_defs, tank_tests, 'jaccards')


if __name__ == "__main__":
    main()
