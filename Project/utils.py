import argparse
import sys


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
Janis Landwehr, 2547715, s9jaland@stud.uni-saarland.de
Sven Stauden, 2549696, s9svstau@stud.uni-saarland.de
Carsten Klaus, 2554140, s8caklau@stud.uni-saarland.de
"""

	print(members)
	sys.exit()


def validate_args(args, ap):
	path_count = len(
		[x for x in (args['train'], args['test']) if x is not None])

	if path_count == 0:
		ap.error('--tr and --te need to be specified')

	if path_count == 1:
		ap.error('--tr and --te must be given together')

	if not (args['accuracy'] or args['list']):
		ap.error('--list or --accuracy need to be specified')



def read_file(path):
	
	input = open(path, encoding="utf8")
	for instance in input:
		instance = instance.strip()
		print(instance)

def generate_suffix_changing_rules(a,b):
	
	assert len(a) == len(b)
	assert a != b
	
	rules = []
	rules.append("$ > $")
	suff_a = ""
	suff_b= ""
	seenStem = False


	for i in range(len(a)-1,-1,-1):
	   
	    # entering prefix
		if seenStem and (a[i] == "_"  or  b[i] == "_"):
			break

		# entering stem
		if not seenStem and a[i] != "_" and b[i] != "_":
			seenStem = True

		suff_a =  (a[i] + suff_a) if a[i] != "_" else suff_a
		suff_b =  (b[i] + suff_b)  if b[i] != "_" else suff_b


		rule = suff_a+"$ > "+suff_b + "$"
		print(rule)
		rules.append(rule)

	return rules

def generate_prefix_changing_rules(a,b):
	assert len(a) == len(b)
	assert a != b
	
	rules = []
	rules.append("$ > $")

	pre_a = "$"
	pre_b = "$"
	for i in range(len(a)):
		if a[i] == "_":
			pre_b += b[i]
		elif b[i] == "_":
			pre_a += a[i]
		else:
			break
	rules.append(pre_a + " > " + pre_b)

	print(rules)
	return rules


